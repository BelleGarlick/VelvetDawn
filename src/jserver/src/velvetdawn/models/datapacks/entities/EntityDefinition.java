package velvetdawn.models.datapacks.entities;

import velvetdawn.VelvetDawn;
import velvetdawn.mechanics.Triggers;
import velvetdawn.mechanics.abilities.Abilities;
import velvetdawn.mechanics.upgrades.Upgrades;
import velvetdawn.models.anytype.AnyBool;
import velvetdawn.models.anytype.AnyFloat;
import velvetdawn.models.instances.attributes.Attributes;
import velvetdawn.models.instances.tags.Tags;
import velvetdawn.utils.Json;

import java.util.List;
import java.util.Set;

import static velvetdawn.Constants.ENTITY_DEFAULT_COMBAT_ATTACK;
import static velvetdawn.Constants.ENTITY_DEFAULT_COMBAT_DEFENSE;
import static velvetdawn.Constants.ENTITY_DEFAULT_COMBAT_RANGE;
import static velvetdawn.Constants.ENTITY_DEFAULT_COMBAT_RELOAD;
import static velvetdawn.Constants.ENTITY_DEFAULT_HEALTH_MAX;
import static velvetdawn.Constants.ENTITY_DEFAULT_MOVEMENT_RANGE;

public class EntityDefinition {

    private static final Set<String> ValidEntityKeys = Set.of(
            "id", "name", "abstract", "extends", "upgrades", "health",
            "movement", "combat", "tags", "notes", "textures", "triggers",
            "commander", "influence", "attributes", "description", "abilities"
    );
    private static final Set<String> ValidHealthKeys = Set.of("max", "notes");
    private static final Set<String> ValidCombatKeys = Set.of("range", "attack", "defense", "reload", "notes");
    private static final Set<String> ValidMovementKeys = Set.of("range", "notes");

    public final String id;
    public final String name;
    public final boolean commander;
    public final String description;

    public final Tags tags = new Tags();
    public final Attributes attributes = new Attributes();
    public final EntityTextures textures = new EntityTextures();

    public final Triggers triggers = new Triggers();
    public final Upgrades upgrades = new Upgrades();
    public final Abilities abilities = new Abilities();

    public EntityDefinition(String id, String name, boolean commander, String description) {
        this.id = id;
        this.name = name;
        this.commander = commander;
        this.description = description;
    }

    /** Parse the entity health data, see wiki for more information. */
    public void parseHealth(String datapackId, Attributes attributes, Json parentJson) throws Exception {
        Json data = parentJson.getJson("health", new Json(),
                String.format("%s health must be a json object", datapackId));

        if (data == null)
            return;

        for (String key: data.keys()) {
            if (!ValidHealthKeys.contains(key))
                throw new Exception(String.format("Invalid health key '%s' on '%s'", key, datapackId));
        }
        // Extract and validate
        AnyFloat max = data.get("max", new AnyFloat(ENTITY_DEFAULT_HEALTH_MAX))
                .validateInstanceIsFloat(String.format("%s max health must be a number", datapackId))
                .validateMinimum(0, String.format("%s max health must be at least 0", datapackId));

        if (max.lte(new AnyFloat(0f)))
            throw new Exception(String.format("%s max health must be greater than 0", datapackId));

        // Set values
        attributes.set("health", "Health", "base:textures.ui.icons.health.png", max);
        attributes.set("health.max", max);
    }

    /** Parse the entity combat data, see wiki for more information. */
    public void parseCombat(String datapackId, Attributes attributes, Json data) throws Exception {
        if (data == null)
            return;

        for (String key: data.keys()) {
            if (!ValidCombatKeys.contains(key))
                throw new Exception(String.format("Invalid combat key '%s' on '%s'", key, datapackId));
        }

        // Extract and validate
        AnyFloat range = data.get("range", new AnyFloat(ENTITY_DEFAULT_COMBAT_RANGE))
                .validateInstanceIsFloat(String.format("%s combat range must be a number", datapackId))
                .validateMinimum(0, String.format("%s combat range must be at least 0", datapackId));

        AnyFloat attack = data.get("attack", new AnyFloat(ENTITY_DEFAULT_COMBAT_ATTACK))
                .validateInstanceIsFloat(String.format("%s combat attack must be a number", datapackId))
                .validateMinimum(0, String.format("%s combat attack must be at least 0", datapackId));

        AnyFloat defence = data.get("defence", new AnyFloat(ENTITY_DEFAULT_COMBAT_DEFENSE))
                .validateInstanceIsFloat(String.format("%s combat defence must be a number", datapackId))
                .validateMinimum(0, String.format("%s combat defence must be at least 0", datapackId));

        AnyFloat reload = data.get("reload", new AnyFloat(ENTITY_DEFAULT_COMBAT_RELOAD))
                .validateInstanceIsFloat(String.format("%s combat reload must be a number", datapackId))
                .validateMinimum(0, String.format("%s combat reload must be at least 0", datapackId));

        // Set
        attributes.set("combat.attack", "Attack", "base:textures.ui.icons.attack.png", attack);
        attributes.set("combat.defense", "Defense", "base:textures.ui.icons.defense.png", defence);
        attributes.set("combat.range", range);
        attributes.set("combat.reload", reload);
        attributes.set("combat.can-attack", new AnyBool(false));
        attributes.set("combat.cooldown", new AnyFloat(0));  // set to 0 so that can-attack will be trigger to on
    }

    /** Parse the entity movement data, see wiki for more information.*/
    private void parseMovement(String datapackId, Attributes attributes, Json data) throws Exception {
        if (data == null)
            return;

        for (String key: data.keys()) {
            if (!ValidMovementKeys.contains(key))
               throw new Exception(String.format("Invalid movement key '%s' on '%s'", key, datapackId));
        }

        // Extract and validate
        AnyFloat range = data.get("range", new AnyFloat(ENTITY_DEFAULT_MOVEMENT_RANGE))
                .validateInstanceIsFloat(String.format("%s movement range must be a number", datapackId))
                .validateMinimum(0, String.format("%s movement range must be at least 0", datapackId));

        // Set
        attributes.set("movement.remaining", new AnyFloat(0));
        attributes.set("movement.range", range);
    }

    public static EntityDefinition fromJson(VelvetDawn velvetDawn, String datapackId, Json json) throws Exception {
        for (String key: json.keys()) {
            if (!ValidEntityKeys.contains(key))
                throw new Exception(String.format("Invalid movement key '%s' on '%s'", key, datapackId));
        }

        var isCommander = json.get("commander", new AnyBool(false))
                .validateInstanceIsBool(String.format("'commander' in %s must be a boolean", datapackId)).toBool();
        String description = json.get("description")
                .validateInstanceIsStringOrNull(String.format("Description in %s must be a string", datapackId))
                .toString();

        var entity = new EntityDefinition(
                datapackId,
                json.get("name")
                        .validateInstanceIsString(String.format("%s name is invalid", datapackId)).value,
                isCommander,
                description
        );

        entity.textures.fromJson(datapackId, json);

        entity.parseHealth(datapackId, entity.attributes, json);

        entity.parseMovement(datapackId, entity.attributes,
                json.getJson("movement", new Json(),
                        String.format("%s movement must be a json object", datapackId)));

        entity.parseCombat(datapackId, entity.attributes,
                json.getJson("combat", new Json(),
                        String.format("%s combat must be a json object", datapackId)));

        entity.tags.load(json.getStringList("tags", List.of(), String.format(
                "Tags in '%s' are invalid. Tags must be a list of strings.", datapackId)));

        entity.triggers.load(velvetDawn, datapackId, json.getJson("triggers", new Json(), String.format(
                "Triggers in '%s' are invalid. Triggers must be a json object.", datapackId)));

        entity.attributes.load(velvetDawn, datapackId, json);

        entity.abilities.load(velvetDawn, datapackId, json.getStrictJsonList("abilities", List.of(), String.format(
                "Abilities in '%s' are invalid. Abilities must be a list of json objects.", datapackId)));

        entity.upgrades.load(velvetDawn, datapackId, json.getStrictJsonList("upgrades", List.of(), String.format(
                "Upgrades in '%s' are invalid. Upgrades must be a list of json objects.", datapackId)));

        return entity;
    }
}
