# Project Assets

This directory contains visual assets for the project documentation.

## Screenshots

- `demo-screenshot.png` - Main web interface screenshot
- `ui-screenshot.png` - Detailed UI view
- `results-example.png` - Example classification results

## Diagrams

- `architecture.png` - System architecture diagram
- `pipeline.png` - ML pipeline flowchart
- `workflow.png` - Development workflow

## Demo

- `demo.gif` - Animated demo of the web interface

## Creating Screenshots

To create screenshots for this project:

1. Start the web interface:
   ```bash
   make run-ui
   ```

2. Open browser to `http://localhost:5001`

3. Take screenshots showing:
   - Main interface with example message
   - Spam classification result (red)
   - Ham classification result (green)
   - Example messages section

## Creating Demo GIF

Use tools like:
- [LICEcap](https://www.cockos.com/licecap/) (Windows/Mac)
- [Peek](https://github.com/phw/peek) (Linux)
- [ScreenToGif](https://www.screentogif.com/) (Windows)

Record a short demo:
1. Enter a message
2. Click classify
3. Show result
4. Try an example message

Keep GIF under 5MB for GitHub display.

## Note

Actual image files should be added here when available. README.md references these files for documentation purposes.
