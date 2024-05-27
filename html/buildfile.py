from pathlib import Path
rootpath = Path(__file__).parent
indexPath = rootpath / "index.html"
visPath = rootpath / "vis-network.min.js"
distPath = rootpath / "dist"
distPath.mkdir(parents=True, exist_ok=True)
distIndexPath = distPath / "index.html"

indexcontent = indexPath.read_text()
viscontent = visPath.read_text()

# Insert the vis-network.min.js script into the index.html file at the "//<Insert here> comment
distcontent = indexcontent.replace("//<Insert here>", viscontent)

# Write the modified index.html file to the dist folder
distIndexPath.write_text(distcontent)
