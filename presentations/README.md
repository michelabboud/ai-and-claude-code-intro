# Presentations

This directory contains slide decks for each chapter. The presentations are written in Marp markdown format, which can be:

1. **Viewed directly** in VS Code with the Marp extension
2. **Converted to PowerPoint** using Marp CLI or GitHub Actions
3. **Exported to PDF** for sharing
4. **Presented directly** in the browser

---

## Generate PowerPoint (Recommended)

### Using GitHub Actions (Easiest)

1. Go to the repository on GitHub
2. Click **Actions** tab
3. Select **"Generate PowerPoint Presentations"** workflow
4. Click **"Run workflow"**
5. Choose options:
   - `commit_files: false` → Download as artifact (default)
   - `commit_files: true` → Commit PPTX files to `presentations/pptx/`
6. Download the `powerpoint-presentations` artifact when complete

### Using Marp CLI (Local)

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

---

## Viewing in Browser

```bash
# Start presentation server
marp -s .

# Then open http://localhost:8080
```

---

## Files

| File | Chapter | Topic |
|------|---------|-------|
| [slides-chapter-01.md](./slides-chapter-01.md) | 1 | Introduction to AI |
| [slides-chapter-02.md](./slides-chapter-02.md) | 2 | Understanding LLMs and Tokens |
| [slides-chapter-03.md](./slides-chapter-03.md) | 3 | The Art of Prompting |
| [slides-chapter-04-05.md](./slides-chapter-04-05.md) | 4-5 | AI Models & Introduction to Claude |
| [slides-chapter-06-08.md](./slides-chapter-06-08.md) | 6-8 | Claude Code (Basic to Professional) |
| [slides-chapter-10-11.md](./slides-chapter-10-11.md) | 10-11 | MCP Protocol (Fundamentals & Server Development) |
| [slides-chapter-12.md](./slides-chapter-12.md) | 12 | AI for DevOps |
| [slides-chapter-15-16.md](./slides-chapter-15-16.md) | 15-16 | Multi-Agent Orchestration |
| [slides-chapter-17-18.md](./slides-chapter-17-18.md) | 17-18 | AIOps (Fundamentals & Advanced) |
| [slides-chapter-19.md](./slides-chapter-19.md) | 19 | Team Transformation |
| [slides-chapter-20.md](./slides-chapter-20.md) | 20 | Agent Loop Detection & Prevention |
| [slides-chapter-21.md](./slides-chapter-21.md) | 21 | Resilience Patterns for Agents |
| [slides-chapter-23.md](./slides-chapter-23.md) | 23 | RAG Fundamentals |
| [slides-chapter-24.md](./slides-chapter-24.md) | 24 | RAG Search & Retrieval Optimization |
