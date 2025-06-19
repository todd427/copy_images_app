const fs = require("uxp").storage.localFileSystem;
const photoshop = require("photoshop");
const app = photoshop.app;

async function selectFolder() {
    return await fs.getFolder();
}

async function loadRotations() {
    const file = await fs.getFileForOpening({ types: ["csv"] });
    if (!file) return {};

    const data = await file.read();
    const rotations = {};

    data.split(/\r?\n/).forEach(line => {
        const [path, angle] = line.split(",");
        if (path && angle) {
            rotations[path.trim()] = parseInt(angle.trim());
        }
    });

    return rotations;
}

async function runBatch(inputFolder, outputFolder, rotations, log) {
    const entries = await inputFolder.getEntries();

    for (const entry of entries) {
        if (entry.isFolder) {
            const subInput = entry;
            const subOutput = await outputFolder.createFolder(entry.name, { overwrite: true });
            await runBatch(subInput, subOutput, rotations, log);
        } else {
            if (!entry.name.match(/\.(jpg|jpeg|png|psd|tif|tiff)$/i)) continue;

            try {
                const doc = await app.open(entry);

                // Rotate if needed
                const rot = rotations[entry.nativePath] || 0;
                if (rot !== 0) {
                    await doc.rotateCanvas(rot);
                }

                // Auto Color
                await app.activeDocument.activeLayers[0].autoColor();

                // Save as JPG
                const saveFile = await outputFolder.createFile(entry.name.replace(/\.[^.]+$/, ".jpg"), { overwrite: true });
                await doc.saveAs(saveFile, { quality: 12 });

                await doc.closeWithoutSaving();
                log("Processed: " + entry.name);
            } catch (e) {
                log("ERROR: " + entry.name + " - " + e);
            }
        }
    }
}

export default {
    selectFolder,
    loadRotations,
    runBatch
};
