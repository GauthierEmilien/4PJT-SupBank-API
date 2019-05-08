let mongoose = require("mongoose");
// const BlockChainModel = mongoose.model('BlockChain');
let BlockChainModel = require("./model");
mongoose.model('BlockChain', BlockChainModel);
//Connect to DB
mongoose.connect("mongodb://localhost:27017/blockChain", (err) => {
    if (err)
        return console.log("Cannot connect to DB");
    console.log("Database is Connected");
    connectionCallback();
});
let connectionCallback = () => {};

module.exports.onConnect = (callback) => {
    connectionCallback = callback;
};