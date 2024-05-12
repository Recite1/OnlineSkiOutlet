const express = require('express');
const app = express();
const cors = require('cors');
const {MongoClient} = require("mongodb");

app.use(cors());

app.get("/sportinglife", async (req,res) => {
    slkCollection.find().toArray()
        .then(result => {
            res.json({ "itemInfo": result});
        })
})

app.get("/evo", async (req,res) => {
    evoCollection.find().toArray()
        .then(result => {
            res.json({ "itemInfo": result});
        })
})

app.get("/updatedTime", async (req,res) => {
    timeCollection.find().toArray()
        .then(result => {
            res.json({ "timeInfo": result});
        })
})

// uri - MongoDB deployment's connection 
const uri = "YOUR MANGODB URL (CONNECTION STRING)";
// Create a new client and connect to MongoDB
const client = new MongoClient(uri);
let db = client.db("SkiItems");
const slkCollection = db.collection("SportingLifeSkis");
const evoCollection = db.collection("EvoSkis");
const timeCollection = db.collection("DateUpdated");

async function run() {
	console.log("Server listening at http://localhost:4000")
	app.listen(4000);

}
// Run the function and handle any errors
run().catch(console.dir);