# Presentations

This directory contains slide decks for each chapter. The presentations are written in Marp markdown format, which can be:

1. **Viewed directly** in VS Code with the Marp extension
2. **Converted to PowerPoint** using Marp CLI
3. **Exported to PDF** for sharing
4. **Presented directly** in the browser

## Converting to PowerPoint

```bash
# Install Marp CLI
npm install -g @marp-team/marp-cli

# Convert to PowerPoint
marp slides-chapter-01.md --pptx -o chapter-01.pptx

# Convert all slides
for f in slides-chapter-*.md; do
  marp "$f" --pptx -o "${f%.md}.pptx"
done

# Convert to PDF
marp slides-chapter-01.md --pdf -o chapter-01.pdf
```

## Viewing in Browser

```bash
# Start presentation server
marp -s .

# Then open http://localhost:8080
```

## Files

| File | Chapter | Topic |
|------|---------|-------|
| [slides-chapter-01.md](./slides-chapter-01.md) | 1 | Introduction to AI |
| [slides-chapter-02.md](./slides-chapter-02.md) | 2 | Understanding LLMs and Tokens |
| [slides-chapter-03.md](./slides-chapter-03.md) | 3 | The Art of Prompting |
| [slides-chapter-04.md](./slides-chapter-04.md) | 4 | AI Models Landscape |
| [slides-chapter-05.md](./slides-chapter-05.md) | 5 | Introduction to Claude |
| [slides-chapter-06-08.md](./slides-chapter-06-08.md) | 6-8 | Claude Code (Basic to Pro) |
| [slides-chapter-09.md](./slides-chapter-09.md) | 9 | MCP Deep Dive |
| [slides-chapter-10.md](./slides-chapter-10.md) | 10 | AI for DevOps |
