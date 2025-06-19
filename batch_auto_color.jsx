// batch_auto_color.jsx
// Photoshop JSX script: Recursive Auto Color (White Balance) Batch Processor

#target photoshop

function processFolder(inputFolder, outputRoot) {
    var files = inputFolder.getFiles();

    for (var i = 0; i < files.length; i++) {
        var file = files[i];

        if (file instanceof Folder) {
            // Recurse into subfolder
            var newSubFolder = new Folder(outputRoot + "/" + file.name);
            if (!newSubFolder.exists) newSubFolder.create();

            processFolder(file, newSubFolder);
        } else if (file instanceof File && isImageFile(file)) {
            processFile(file, outputRoot);
        }
    }
}

function isImageFile(file) {
    var name = file.name.toLowerCase();
    return name.match(/\.(jpg|jpeg|png|psd|tif|tiff)$/);
}

function processFile(file, outputFolder) {
    try {
        var doc = app.open(file);

        // Apply Auto Color (acts like Auto White Balance)
        doc.activeLayer = doc.layers[0];
        doc.activeLayer.autoColor();

        // Save output as JPG (you can change this to PNG, etc.)
        var saveFile = new File(outputFolder + "/" + file.name.replace(/\.[^.]+$/, ".jpg"));
        var opts = new JPEGSaveOptions();
        opts.quality = 12;

        doc.saveAs(saveFile, opts, true);
        doc.close(SaveOptions.DONOTSAVECHANGES);

        $.writeln("Processed: " + file.fullName);
    } catch (e) {
        $.writeln("ERROR processing: " + file.fullName + " - " + e);
    }
}

// Main entry

var inputFolder = Folder.selectDialog("Select input folder");
var outputFolder = Folder.selectDialog("Select output folder");

if (inputFolder && outputFolder) {
    $.writeln("Processing folder: " + inputFolder.fsName);
    processFolder(inputFolder, outputFolder);
    $.writeln("DONE.");
} else {
    $.writeln("Cancelled.");
}
