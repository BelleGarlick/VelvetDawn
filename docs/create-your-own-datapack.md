# Creating Datapacks
Datapacks are designed to be flexible, modular extendable and easy.
To create your own datapack, simply open the datapacks folder, create a new folder named 'my-datapack'.
Congratulations! You've just made your own datapack.

#### Contents
1. Entities
2. Tiles
3. Resources
4. Behaviours
   1. Triggers
   2. Abilities
   3. Influence
   4. Upgrades
   5. Targets
   6. Conditions
   7. Modifiers
   8. Execute
5. Advanced
   1. Tags
   2. Overriding
   3. Extending

## Entities

## Tiles

## Resources

## Behaviours
### Triggers
### Abilities
### Influence
### Upgrades

### Targets
### Conditions
### Modifiers
### Execute

## Advanced

### Tags
Tags are a way to help interoperability between datapacks. 
They can be used as a placeholder to define a generic unit that may be used.

For example, each tile defines its neighbours. 
Without knot knowing all possible datapacks there could possibly be, it would be impossible to allow
your datapack to seamlessly connect to another pack's tiles. 
However, tags allow you to define that a given tile may connect to a, for example, 'tag:deep_water'.
Any tile which contains the tag 'tag:water' may be used. 

All tags will be prefixed with "tag:" if not already given.

### Overriding
Overriding allows your datapack to modify or be modified by another datapack (order will be chosen based on the config file).

By default, tiles, entities and resources will be assigned an id based on the file name prefixed with the datapack name. 
e.g. `velvet-dawn/entities/example.json` becomes `velvet-dawn:example`.
The recommended way to assign an id is to declare it in the json definition with the key `id`.
However, for resources (which have on json) it is possible to assign the prefix with the file name.
If the file already contains a prefix (denoted by `{prefix}_{name}`) then the entity will not be given another prefix.
This means, `my-datapack/entities/velvet-dawn_example.json` will be assigned the id `velvet-dawn:example`, thus overriding the original entity.

By overriding the entities id, your custom entity will take its place everywhere.
This may lead to unexpected behaviour - particularly when many datapacks overriding things are loaded.
This functionality is expected to be used only for overriding resource files but may be used throughout datapacks.

**Example of entity/tile id overriding**
```json
{
   "id": "velvet-dawn:example",
   "name": "Example"
}
```

### Extending
Datapacks allow for polymorphism making it far easier to construct
entities and files which share common features. For example, you may
want all your entities to all have an upgrade path for upgrading their max health.
It would be laborious store this in each file and particularly error-prone if you wanted to change all the values.
Instead, extending allows you to store one file with this upgrade path with all entities refer to.
Only file marked as `abstract` may be extended.

Only specific entities or tiles may be extended, tags will not work.

It may also be easier to name all your abstract files prefixed with '_' (although this has no affect on the game).

**Example**  
`my-datapack/entities/_max-health.json`
```json
{
   "abstract": true,
   "health": {
      "max": 100
   }
}
```
`my-datapack/entities/entity_a.json`
```json
{
   "name": "Entity a",
   "extends": ["my-datapack:_max-health"]
}
```
`my-datapack/entities/entity_b.json`
```json
{
   "name": "Entity b",
   "extends": ["my-datapack:_max-health"]
}
```