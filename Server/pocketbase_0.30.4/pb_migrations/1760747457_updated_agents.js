/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_2726680096")

  // add field
  collection.fields.addAt(17, new Field({
    "hidden": false,
    "id": "json1481674436",
    "maxSize": 0,
    "name": "installed_programs",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  // add field
  collection.fields.addAt(18, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text2736858503",
    "max": 0,
    "min": 0,
    "name": "antivirus",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // add field
  collection.fields.addAt(19, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text1208032126",
    "max": 0,
    "min": 0,
    "name": "firewall",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // add field
  collection.fields.addAt(20, new Field({
    "hidden": false,
    "id": "number2384979105",
    "max": null,
    "min": null,
    "name": "pending_updates",
    "onlyInt": false,
    "presentable": false,
    "required": false,
    "system": false,
    "type": "number"
  }))

  // add field
  collection.fields.addAt(21, new Field({
    "hidden": false,
    "id": "date2153816109",
    "max": "",
    "min": "",
    "name": "last_patch",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "date"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_2726680096")

  // remove field
  collection.fields.removeById("json1481674436")

  // remove field
  collection.fields.removeById("text2736858503")

  // remove field
  collection.fields.removeById("text1208032126")

  // remove field
  collection.fields.removeById("number2384979105")

  // remove field
  collection.fields.removeById("date2153816109")

  return app.save(collection)
})
