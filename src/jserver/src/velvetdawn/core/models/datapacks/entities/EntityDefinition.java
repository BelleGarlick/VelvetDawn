package velvetdawn.core.models.datapacks.entities;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.constants.AttributeValues;
import velvetdawn.core.mechanics.Triggers;
import velvetdawn.core.mechanics.abilities.Abilities;
import velvetdawn.core.mechanics.upgrades.Upgrades;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyBool;
import velvetdawn.core.models.anytype.AnyFloat;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.anytype.AnyList;
import velvetdawn.core.models.anytype.AnyString;
import velvetdawn.core.models.instances.attributes.Attributes;
import velvetdawn.core.models.instances.attributes.AttributesDefinition;

import java.util.HashSet;
import java.util.Set;

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

    public final Set<String> tags = new HashSet<>();
    public final AttributesDefinition attributes = new AttributesDefinition();
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
    public void parseHealth(AnyJson parentJson) throws Exception {
        AnyJson data = parentJson.get("health", new AnyJson())
                .validateInstanceIsJson(String.format("%s health must be a json object", this.id));

        if (data == null)
            return;

        for (String key: data.keys()) {
            if (!ValidHealthKeys.contains(key))
                throw new Exception(String.format("Invalid health key '%s' on '%s'", key, this.id));
        }
        // Extract and validate
        AnyFloat max = data.get("max", new AnyFloat(AttributeValues.DefaultEntityHealthMax))
                .validateInstanceIsFloat(String.format("%s max health must be a number", this.id))
                .validateMinimum(0, String.format("%s max health must be at least 0", this.id));

        if (max.lte(new AnyFloat(0f)))
            throw new Exception(String.format("%s max health must be greater than 0", this.id));

        // Set values
        attributes.set("health", "Health", "base:textures.ui.icons.health.png", max);
        attributes.set("health.max", max);
    }

    /** Parse the entity combat data, see wiki for more information. */
    public void parseCombat(AnyJson json) throws Exception {
        var data = json.get("combat", new AnyJson())
            .validateInstanceIsJson(String.format("%s combat must be a json object", this.id));

        if (data == null)
            return;

        for (String key: data.keys()) {
            if (!ValidCombatKeys.contains(key))
                throw new Exception(String.format("Invalid combat key '%s' on '%s'", key, this.id));
        }

        // Extract and validate
        AnyFloat range = data.get("range", new AnyFloat(AttributeValues.DefaultEntityCombatRange))
                .validateInstanceIsFloat(String.format("%s combat range must be a number", this.id))
                .validateMinimum(0, String.format("%s combat range must be at least 0", this.id));

        AnyFloat attack = data.get("attack", new AnyFloat(AttributeValues.DefaultEntityCombatAttack))
                .validateInstanceIsFloat(String.format("%s combat attack must be a number", this.id))
                .validateMinimum(0, String.format("%s combat attack must be at least 0", this.id));

        AnyFloat defense = data.get("defense", new AnyFloat(AttributeValues.DefaultEntityCombatDefense))
                .validateInstanceIsFloat(String.format("%s combat defence must be a number", this.id))
                .validateMinimum(0, String.format("%s combat defence must be at least 0", this.id));

        AnyFloat reload = data.get("reload", new AnyFloat(AttributeValues.DefaultEntityCombatReload))
                .validateInstanceIsFloat(String.format("%s combat reload must be a number", this.id))
                .validateMinimum(0, String.format("%s combat reload must be at least 0", this.id));

        // Set
        attributes.set("combat.attack", "Attack", "base:textures.ui.icons.attack.png", attack);
        attributes.set("combat.defense", "Defense", "base:textures.ui.icons.defense.png", defense);
        attributes.set("combat.range", range);
        attributes.set("combat.reload", reload);
        attributes.set("combat.can-attack", new AnyBool(false));
        attributes.set("combat.cooldown", new AnyFloat(0));  // set to 0 so that can-attack will be trigger to on
    }

    /** Parse the entity movement data, see wiki for more information.*/
    public void parseMovement(AnyJson json) throws Exception {
        var data = json.get("movement", new AnyJson())
                .validateInstanceIsJson(String.format("%s movement must be a json object", this.id));

        if (data == null)
            return;

        for (String key: data.keys()) {
            if (!ValidMovementKeys.contains(key))
               throw new Exception(String.format("Invalid movement key '%s' on '%s'", key, this.id));
        }

        // Extract and validate
        AnyFloat range = data.get("range", new AnyFloat(AttributeValues.DefaultEntityMovementRange))
                .validateInstanceIsFloat(String.format("%s movement range must be a number", this.id))
                .validateMinimum(0, String.format("%s movement range must be at least 0", this.id));

        // Set
        attributes.set("movement.remaining", new AnyFloat(0));
        attributes.set("movement.range", range);
    }

    public static EntityDefinition fromJson(VelvetDawn velvetDawn, String datapackId, AnyJson json) throws Exception {
        for (String key: json.keys()) {
            if (!ValidEntityKeys.contains(key))
                throw new Exception(String.format("Invalid movement key '%s' on '%s'", key, datapackId));
        }

        var isCommander = json.get("commander", new AnyBool(false))
                .validateInstanceIsBool(String.format("'commander' in %s must be a boolean", datapackId)).toBool();

        String description = null;
        if (json.get("description") instanceof AnyString)
            description = ((AnyString) json.get("description")).value;

        var entity = new EntityDefinition(
                datapackId,
                json.get("name")
                        .validateInstanceIsString(String.format("%s name is invalid", datapackId)).value,
                isCommander,
                description
        );

        entity.textures.fromJson(datapackId, json);

        entity.parseHealth(json);
        entity.parseMovement(json);
        entity.parseCombat(json);

        var tags = json.get("tags", Any.list())
                .validateInstanceIsList(String.format("Tags in '%s' are invalid. Tags must be a list of strings.", datapackId));

        for (Any item: tags.items)
            entity.tags.add(item
                    .validateInstanceIsString(String.format("Error in %s. Tags must be strings.", datapackId))
                    .toString());

        entity.triggers.load(
                velvetDawn,
                datapackId,
                json.get("triggers", new AnyJson())
                        .validateInstanceIsJson(String.format(
                        "Triggers in '%s' are invalid. Triggers must be a json object.", datapackId)));

        entity.attributes.load(velvetDawn, datapackId, json);

        entity.abilities.load(
                velvetDawn,
                datapackId,
                json.get("abilities", new AnyList())
                        .validateInstanceIsList(String.format(
                "Abilities in '%s' are invalid. Abilities must be a list of json objects.", datapackId)));

        entity.upgrades.load(velvetDawn, datapackId, json.get("upgrades", Any.list()).validateInstanceIsList(String.format(
                "Upgrades in '%s' are invalid. Upgrades must be a list of json objects.", datapackId)));

        return entity;
    }
    public AnyJson json() {
        return new AnyJson()
                .set("id", this.id)
                .set("name", this.name)
                .set("commander", this.commander)
                .set("description", this.description)
                .set("textures", this.textures.toJson());
    }
}
