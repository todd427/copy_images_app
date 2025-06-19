import batchProcessor from "./batch_auto_color.js";

const inputBtn = document.getElementById("inputFolder");
const outputBtn = document.getElementById("outputFolder");
const runBtn = document.getElementById("runProcess");
const logElem = document.getElementById("log");

let inputFolder = null;
let outputFolder = null;
let rotations = {};

inputBtn.addEventListener("click", async () => {
    inputFolder = await batchProcessor.selectFolder();
    log("Selected Input: " + inputFolder.nativePath);
});

outputBtn.addEventListener("click", async () => {
    outputFolder = await batchProcessor.selectFolder();
    log("Selected Output: " + outputFolder.nativePath);
});

runBtn.addEventListener("click", async () => {
    if (!inputFolder || !outputFolder) {
        log("Please select both Input and Output folders.");
        return;
    }

    const loadRotations = document.getElementById("loadRotations").checked;
    if (loadRotations) {
        rotations = await batchProcessor.loadRotations();
        log(`Loaded rotations: ${Object.keys(rotations).length} entries`);
    }

    await batchProcessor.runBatch(inputFolder, outputFolder, rotations, log);
});

function log(message) {
    logElem.textContent += message + "\n";
}
