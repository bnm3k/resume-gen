# Resume builder
Simple resume builder based on [mikepqr's](https://github.com/mikepqr/resuame.md)
resume builder. Write your resume in `resume.md`, style it in `style.css`, then
output to html. Will support output to pdf in future.
For use in linux-based systems since that's what I am working on.

## Live reload
There is a couple of helpers for live-reloading while editing. To try out
live-reloading, run `make watch`.
Currently live-reloading is set up for Firefox and vim since those are my go-to
tools.
Remember to source `refresh/auto.vim` to set up the autocmds for writing
buffers.
Currently, live-reloading is very hacky, and quite slow when you're making
edits in normal mode. It's set up using [entr](https://eradman.com/entrproject/)
which runs a given command when the specified files change. All other
live-reloading tools I've tried out just didn't work out as I wanted right out
of the box and since I did not want to spend too much time on this, I opted
for 'hacky'. Suggestions are welcome though, specifically, live-reloading on
vim buffer change without having to write to disk first to communicate to
downstream tools to refresh.
