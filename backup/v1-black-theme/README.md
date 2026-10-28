# V1 black-theme backup (rollback copy)

This is the original G Con Associates **V1 black-themed** website, exactly as it was
served at https://gcon-associates.pages.dev/ before V2 replaced it.

- `index.html` is the complete site (single self-contained file). It is byte-identical to the
  live Cloudflare Pages deployment at the time of backup (SHA-1 `bc2b073a051d955f2f1cb4655f38141d29b65ae1`)
  and to commit `b93a9b6` ("Update G Con Associates website per client feedback") of the V1 repo
  `nelbinxav/gcon-associates`.
- It is preserved only as a rollback copy. **Do not edit it.**
- V2 (the blue-themed site in the repository root) is now the production version and replaces this on Cloudflare.

## Restore

Deploy this folder to the Cloudflare Pages project `gcon-associates`, e.g.
`npx wrangler pages deploy backup/v1-black-theme --project-name gcon-associates`.
This folder is not part of the GitHub Pages artifact (the workflow copies a fixed file list).
