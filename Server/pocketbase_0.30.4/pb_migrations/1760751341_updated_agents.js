/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_2726680096")

  // remove field
  collection.fields.removeById("text2736858503")

  // add field
  collection.fields.addAt(21, new Field({
    "hidden": false,
    "id": "json2736858503",
    "maxSize": 0,
    "name": "antivirus",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_2726680096")

  // add field
  collection.fields.addAt(17, new Field({
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

  // remove field
  collection.fields.removeById("json2736858503")

  return app.save(collection)
})
