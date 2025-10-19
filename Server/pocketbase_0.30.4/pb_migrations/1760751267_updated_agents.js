/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_2726680096")

  // remove field
  collection.fields.removeById("text2783163181")

  // add field
  collection.fields.addAt(21, new Field({
    "hidden": false,
    "id": "json2783163181",
    "maxSize": 0,
    "name": "ip",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_2726680096")

  // add field
  collection.fields.addAt(12, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text2783163181",
    "max": 0,
    "min": 0,
    "name": "ip",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // remove field
  collection.fields.removeById("json2783163181")

  return app.save(collection)
})
