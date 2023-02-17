import velvet_dawn.db.units
from test.base_test import BaseTest
from velvet_dawn.models.coordinate import Coordinate


class TestDbUnits(BaseTest):

    def test_spawn_and_remove(self):
        velvet_dawn.datapacks.init(self.get_config())
        commander_def = velvet_dawn.datapacks.entities['testing:commander']

        instance = velvet_dawn.db.units.spawn(commander_def, "1", 0, 0)
        self.assertEqual(1, len(velvet_dawn.db.units.get_all_units()))

        velvet_dawn.db.units.remove(instance)
        self.assertEqual(0, len(velvet_dawn.db.units.get_all_units()))
        self.assertEqual(0, len(velvet_dawn.db.units.get_all_player_units("1")))
        self.assertEqual(0, len(velvet_dawn.db.units.get_units_at_positions(Coordinate(0, 0))))
        self.assertEqual(0, len(velvet_dawn.db.units.get_units_by_unit_id('testing:commander')))
        self.assertIsNone(velvet_dawn.db.units.get_unit_by_instance_id(instance.instance_id))

    def test_move(self):
        velvet_dawn.datapacks.init(self.get_config())
        commander_def = velvet_dawn.datapacks.entities['testing:commander']

        instance = velvet_dawn.db.units.spawn(commander_def, "1", 0, 0)
        velvet_dawn.db.units.move(instance, Coordinate(10.2, 10.3))

        self.assertEqual(0, len(velvet_dawn.db.units.get_units_at_positions(Coordinate(0, 0))))
        self.assertEqual(1, len(velvet_dawn.db.units.get_units_at_positions(Coordinate(10, 10))))

        all_units = velvet_dawn.db.units.get_all_units()
        self.assertTrue(all_units[0].x == 10.2, all_units[0].y == 10.3)
        self.assertTrue(all_units[0].tile_x == 10, all_units[0].tile_y == 10)

        player_units = velvet_dawn.db.units.get_all_player_units("1")
        self.assertTrue(player_units[0].x == 10.2, player_units[0].y == 10.3)
        self.assertTrue(player_units[0].tile_x == 10, player_units[0].tile_y == 10)

        unit_units = velvet_dawn.db.units.get_units_by_unit_id('testing:commander')
        self.assertTrue(unit_units[0].x == 10.2, unit_units[0].y == 10.3)
        self.assertTrue(unit_units[0].tile_x == 10, unit_units[0].tile_y == 10)

        instances = velvet_dawn.db.units.get_unit_by_instance_id(instance.instance_id)
        self.assertTrue(instances.x == 10.2, instances.y == 10.3)
        self.assertTrue(instances.tile_x == 10, instances.tile_y == 10)

    def test_updates(self):
        velvet_dawn.datapacks.init(self.get_config())
        commander_def = velvet_dawn.datapacks.entities['testing:commander']

        instance = velvet_dawn.db.units.spawn(commander_def, "1", 0, 0)
        updates = velvet_dawn.db.units.get_updates()
        self.assertEqual(1, len(updates['updates']))

        # Move to same position wont be a new update
        velvet_dawn.db.units.move(instance, Coordinate(0, 0))
        self.assertEqual(1, len(velvet_dawn.db.units.get_updates()['updates']))

        velvet_dawn.db.units.move(instance, Coordinate(1, 0))
        self.assertEqual(2, len(velvet_dawn.db.units.get_updates()['updates']))

        velvet_dawn.db.units.remove(instance)
        self.assertEqual(1, len(velvet_dawn.db.units.get_updates()['removed']))

    def test_get_all_units(self):
        velvet_dawn.datapacks.init(self.get_config())
        commander_def = velvet_dawn.datapacks.entities['testing:commander']

        velvet_dawn.db.units.spawn(commander_def, "1", 0, 0)
        velvet_dawn.db.units.spawn(commander_def, "1", 0, 0)
        velvet_dawn.db.units.spawn(commander_def, "2", 0, 0)

        self.assertEqual(3, len(velvet_dawn.db.units.get_all_units()))

    def test_get_players_units(self):
        velvet_dawn.datapacks.init(self.get_config())
        commander_def = velvet_dawn.datapacks.entities['testing:commander']

        velvet_dawn.db.units.spawn(commander_def, "1", 0, 0)
        velvet_dawn.db.units.spawn(commander_def, "1", 0, 0)
        velvet_dawn.db.units.spawn(commander_def, "2", 0, 0)

        self.assertEqual(2, len(velvet_dawn.db.units.get_all_player_units("1")))
        self.assertEqual(1, len(velvet_dawn.db.units.get_all_player_units("2")))

    def test_get_units_at_position(self):
        velvet_dawn.datapacks.init(self.get_config())
        commander_def = velvet_dawn.datapacks.entities['testing:commander']

        velvet_dawn.db.units.spawn(commander_def, "1", 0, 0)

        self.assertEqual(1, len(velvet_dawn.db.units.get_units_at_positions(Coordinate(0, 0))))
        self.assertEqual(0, len(velvet_dawn.db.units.get_units_at_positions(Coordinate(0, 1))))

    def test_get_units_by_id(self):
        velvet_dawn.datapacks.init(self.get_config())
        commander_def = velvet_dawn.datapacks.entities['testing:commander']

        velvet_dawn.db.units.spawn(commander_def, "1", 0, 0)
        velvet_dawn.db.units.spawn(commander_def, "1", 0, 1)

        self.assertEqual(2, len(velvet_dawn.db.units.get_units_by_unit_id('testing:commander')))

    def test_get_unit_by_instance_id(self):
        velvet_dawn.datapacks.init(self.get_config())
        commander_def = velvet_dawn.datapacks.entities['testing:commander']

        instance = velvet_dawn.db.units.spawn(commander_def, "1", 0, 0)

        self.assertEqual(
            velvet_dawn.db.units.get_unit_by_instance_id(instance.instance_id).instance_id,
            instance.instance_id
        )
