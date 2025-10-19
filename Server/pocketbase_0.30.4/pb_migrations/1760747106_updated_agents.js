/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_2726680096")

  // add field
  collection.fields.addAt(16, new Field({
    "cascadeDelete": false,
    "collectionId": "pbc_2442875294",
    "hidden": false,
    "id": "relation434858273",
    "maxSelect": 1,
    "minSelect": 0,
    "name": "client_id",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "relation"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_2726680096")

  // remove field
  collection.fields.removeById("relation434858273")

  return app.save(collection)
})
