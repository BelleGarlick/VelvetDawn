from velvet_dawn.config import Config, SpawningConfig

import velvet_dawn
from velvet_dawn.dao import app, db
from velvet_dawn.dao.models import SpawnArea
from velvet_dawn.models.coordinate import Coordinate

from test.base_test import BaseTest


class TestMapSpawning(BaseTest):

    def test_lobby_to_setup_create_spawn(self):
        with app.app_context():
            db.session.query(SpawnArea).delete()
            db.session.commit()

            self.assertEqual(0, len(db.session.query(SpawnArea).all()))

            velvet_dawn.players.join("abc", "a")
            velvet_dawn.players.join("bcd", "a")
            config = Config()
            config.spawning = SpawningConfig()
            velvet_dawn.game.phase.start_setup_phase(config)

            self.assertNotEqual(0, len(db.session.query(SpawnArea).all()))

    def test_allocate_spawn_points(self):
        """ We know all other parts work, so here
        were just test the correct number of tiles
        are created to the db per team """
        with app.app_context():
            config = Config().set_map_size(14, 14)
            config.spawning = SpawningConfig().set_spawning(0, 0, 0)

            velvet_dawn.players.join("abc", "a")
            velvet_dawn.players.join("bcd", "a")
            velvet_dawn.map.allocate_spawn_points(config)

            items = db.session.query(SpawnArea).all()
            self.assertEqual(2, len(items))
            self.assertEqual(7, items[0].pos_x)
            self.assertEqual(0, items[0].pos_y)
            self.assertEqual(6, items[1].pos_x)
            self.assertEqual(13, items[1].pos_y)

    def test_allocate_spawn_points_2(self):
        """ Same test as above but with different teams/sizes """
        with app.app_context():
            config = Config().set_map_size(20, 20)
            config.spawning = SpawningConfig().set_spawning(3, 2, 3)

            velvet_dawn.players.join("abc", "a")
            velvet_dawn.players.join("bcd", "a")
            velvet_dawn.map.allocate_spawn_points(config)

            self.assertEqual(128, len(db.session.query(SpawnArea).all()))
            self.assertEqual(64, len(velvet_dawn.map.get_allocated_spawn_area("abc")))
            self.assertTrue(velvet_dawn.map.is_point_spawnable("abc", 10, 0))
            self.assertFalse(velvet_dawn.map.is_point_spawnable("abc", 0, 0))

            self.assertEqual(64, len(velvet_dawn.map.get_allocated_spawn_area("bcd")))
            self.assertTrue(velvet_dawn.map.is_point_spawnable("bcd", 10, 19))
            self.assertFalse(velvet_dawn.map.is_point_spawnable("bcd", 0, 19))

    def test_calculate_full_spawn_half_width(self):
        config = Config()

        # 0 Width
        config.spawning = SpawningConfig().set_spawning(0, 0, 0)
        self.assertEqual(0, velvet_dawn.map.spawn._calculate_spawn_area_half_width(config, 1))
        self.assertEqual(0, velvet_dawn.map.spawn._calculate_spawn_area_half_width(config, 2))

        # Updating width multiplier
        config.spawning = SpawningConfig().set_spawning(3, 0, 0)
        self.assertEqual(3, velvet_dawn.map.spawn._calculate_spawn_area_half_width(config, 1))
        self.assertEqual(6, velvet_dawn.map.spawn._calculate_spawn_area_half_width(config, 2))

        # Updating width addition
        config.spawning = SpawningConfig().set_spawning(3, 2, 0)
        self.assertEqual(5, velvet_dawn.map.spawn._calculate_spawn_area_half_width(config, 1))
        self.assertEqual(8, velvet_dawn.map.spawn._calculate_spawn_area_half_width(config, 2))

        # Updating neighbour multiplier
        config.spawning = SpawningConfig().set_spawning(3, 2, 2)
        self.assertEqual(7, velvet_dawn.map.spawn._calculate_spawn_area_half_width(config, 1))
        self.assertEqual(12, velvet_dawn.map.spawn._calculate_spawn_area_half_width(config, 2))

    def test_get_central_spawn_ordinates(self):
        """ Test the correct central spawn ordinates are layed out correct """
        config = Config().set_map_size(7, 5)
        config.spawning = SpawningConfig().set_spawning(0, 0, 0)

        spawns = velvet_dawn.map.spawn._get_central_spawn_ordinates(config, 1, 1)
        self.assertEqual(spawns[0], Coordinate(3, 0))

        spawns = velvet_dawn.map.spawn._get_central_spawn_ordinates(config, 2, 1)
        self.assertEqual(spawns[0], Coordinate(3, 0))
        self.assertEqual(spawns[1], Coordinate(3, 4))

        spawns = velvet_dawn.map.spawn._get_central_spawn_ordinates(config, 3, 1)
        self.assertEqual(spawns[0], Coordinate(3, 0))
        self.assertEqual(spawns[1], Coordinate(6, 3))
        self.assertEqual(spawns[2], Coordinate(0, 4))

        spawns = velvet_dawn.map.spawn._get_central_spawn_ordinates(config, 4, 1)
        self.assertEqual(spawns[0], Coordinate(3, 0))
        self.assertEqual(spawns[1], Coordinate(6, 2))
        self.assertEqual(spawns[2], Coordinate(3, 4))
        self.assertEqual(spawns[3], Coordinate(0, 2))

    def test_get_central_spawn_ordinates_with_realistic_values(self):
        """ Test the correct central spawn ordinates are layed out correct with
         more realistic size
        """
        config = Config().set_map_size(41, 25)
        config.spawning = SpawningConfig().set_spawning(2, 2, 2)

        spawns = velvet_dawn.map.spawn._get_central_spawn_ordinates(config, 1, 2)
        self.assertEqual(spawns[0], Coordinate(20, 0))

        spawns = velvet_dawn.map.spawn._get_central_spawn_ordinates(config, 2, 2)
        self.assertEqual(spawns[0], Coordinate(20, 0))
        self.assertEqual(spawns[1], Coordinate(20, 24))

        spawns = velvet_dawn.map.spawn._get_central_spawn_ordinates(config, 3, 2)
        self.assertEqual(spawns[0], Coordinate(20, 0))
        self.assertEqual(spawns[1], Coordinate(29, 24))
        self.assertEqual(spawns[2], Coordinate(12, 24))

        spawns = velvet_dawn.map.spawn._get_central_spawn_ordinates(config, 4, 2)
        self.assertEqual(spawns[0], Coordinate(20, 0))
        self.assertEqual(spawns[1], Coordinate(40, 12))
        self.assertEqual(spawns[2], Coordinate(20, 24))
        self.assertEqual(spawns[3], Coordinate(0, 12))

    def test_get_central_spawn_ordinates_too_small(self):
        """ Test spawning is correct when map is too small """
        config = Config().set_map_size(7, 5)
        config.spawning = SpawningConfig().set_spawning(2, 2, 2)

        with self.assertRaises(Exception):
            velvet_dawn.map.spawn._get_central_spawn_ordinates(config, 1, 1)

    def test_get_cell_from_perimeter_index(self):
        """ Test getting the cell based on the perimeter index """
        config_3x3 = Config().set_map_size(3, 3)
        config_4x4 = Config().set_map_size(4, 4)

        correct_points = [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [1, 2], [0, 2], [0, 1]]
        for i in range(8):
            current_point = velvet_dawn.map.spawn._get_cell_from_perimeter_index(i, config_3x3)
            self.assertEqual(current_point.x, correct_points[i][0])
            self.assertEqual(current_point.y, correct_points[i][1])

        correct_points = [
            [0, 0], [1, 0], [2, 0],
            [3, 0], [3, 1], [3, 2],
            [3, 3], [2, 3], [1, 3],
            [0, 3], [0, 2], [0, 1],
        ]
        for i in range(12):
            current_point = velvet_dawn.map.spawn._get_cell_from_perimeter_index(i, config_4x4)
            self.assertEqual(current_point.x, correct_points[i][0])
            self.assertEqual(current_point.y, correct_points[i][1])

    def test_get_next_coordinate(self):
        """ Test looping around the perimeter gives the next item """
        with app.app_context():
            config_3x3 = Config().set_map_size(3, 3)
            config_4x4 = Config().set_map_size(4, 4)

            # clockwise 3x3
            correct_points = [[1, 0], [2, 0], [2, 1], [2, 2], [1, 2], [0, 2], [0, 1], [0, 0]]
            current_point = Coordinate(0, 0)

            for i in range(8):
                current_point = velvet_dawn.map.spawn._get_next_coordinate(current_point, config_3x3)
                self.assertEqual(current_point.x, correct_points[i][0])
                self.assertEqual(current_point.y, correct_points[i][1])

            # anti-clockwise 3x3
            correct_points = [[0, 1], [0, 2], [1, 2], [2, 2], [2, 1], [2, 0], [1, 0], [0, 0]]
            current_point = Coordinate(0, 0)

            for i in range(8):
                current_point = velvet_dawn.map.spawn._get_next_coordinate(current_point, config_3x3, clockwise=False)
                self.assertEqual(current_point.x, correct_points[i][0])
                self.assertEqual(current_point.y, correct_points[i][1])

            # clockwise 4x4
            correct_points = [
                [1, 0], [2, 0], [3, 0],
                [3, 1], [3, 2], [3, 3],
                [2, 3], [1, 3], [0, 3],
                [0, 2], [0, 1], [0, 0]
            ]
            current_point = Coordinate(0, 0)

            for i in range(12):
                current_point = velvet_dawn.map.spawn._get_next_coordinate(current_point, config_4x4)
                self.assertEqual(current_point.x, correct_points[i][0])
                self.assertEqual(current_point.y, correct_points[i][1])

            # anti-clockwise 4x4
            correct_points = [
                [0, 1], [0, 2], [0, 3],
                [1, 3], [2, 3], [3, 3],
                [3, 2], [3, 1], [3, 0],
                [2, 0], [1, 0], [0, 0],
            ]
            current_point = Coordinate(0, 0)

            for i in range(8):
                current_point = velvet_dawn.map.spawn._get_next_coordinate(current_point, config_4x4, clockwise=False)
                self.assertEqual(current_point.x, correct_points[i][0])
                self.assertEqual(current_point.y, correct_points[i][1])
