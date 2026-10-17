# Icon and asset sources

Brand marks are used only to identify the named platforms/technologies. Trademarks belong to their owners.

| Mark(s) | Source |
|---|---|
| Python, FastAPI, React, PostgreSQL, Snowflake, LangChain, LangGraph, MCP, Hugging Face, Docker, Terraform, Jenkins, Git, GitHub, Gmail, Medium, LeetCode, CodeChef | Simple Icons 16.35.0 (CC0 1.0 icon data), https://simpleicons.org |
| LinkedIn | Simple Icons 13.21.0 (the mark was removed from later releases) |
| AWS | @lobehub/icons-static-svg 1.95.1 (`aws.svg`), https://github.com/lobehub/lobe-icons |
| Chroma, Topmate | No mark used (text chip / not included) |

Fonts: Syne and JetBrains Mono, SIL Open Font License 1.1 (see OFL-*.txt), embedded as base64 WOFF2 from @fontsource 5.3.0.
Portraits: author-supplied `id.png` and `right_pointing.png`, embedded unmodified (lossless recompression, pixel-identical).

## Auto-update tooling
`tools/` regenerates `assets/id-dashboard.svg`, `assets/writing.svg` and `assets/footer.svg` from `tools/data/*.json`
(GitHub public API numbers and the writing list). It embeds the same fonts, icons and portrait as above and makes no
network requests when the images render. Run it by hand with `python tools/update.py --offline`.
