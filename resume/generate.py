# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import argparse
import logging
import os
import pathlib
import re
import sys

import markdown

preamble = """\
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
@import url("https://fonts.googleapis.com/css2?family=Nuosu+SIL&display=swap");
{css}
</style>
</head>
<body>
<div id="resume">
"""

postamble = """\
</div>
</body>
</html>
"""


def title(md: str) -> str:
    """
    Return the contents of the first markdown heading in md, which we
    assume to be the title of the document.
    """
    for line in md.splitlines():
        if re.match("^#[^#]", line):  # starts with exactly one '#'
            return line.lstrip("#").strip()
    raise ValueError(
        "Cannot find any lines that look like markdown h1 headings to use as"
        " the title"
    )


def generate_html(md: str, css: str) -> str:
    return "".join(
        (
            preamble.format(title=title(md), css=css),
            markdown.markdown(md, extensions=["smarty"]),
            postamble,
        )
    )


if __name__ == "__main__":
    # parse commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--output-dir", default=os.getcwd(), nargs="?")
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    # config logging level
    if args.quiet:
        log_level = logging.WARN
    elif args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level, format="%(message)s")

    # get output dir for generated html
    output_dir = args.output_dir
    if not os.path.isdir(output_dir):
        sys.stderr.write(f"Invalid path to output dir: {output_dir}\n")
        sys.exit(1)

    resume_dir = pathlib.Path(__file__).parent.resolve()

    # get resume markdown content
    resume_markdown_path = os.path.join(resume_dir, "resume.md")
    with open(resume_markdown_path, encoding="utf-8") as f:
        resume_markdown = f.read()

    # get css for styling resume
    css_path = os.path.join(resume_dir, "style.css")
    with open(css_path, encoding="utf-8") as f:
        css = f.read()

    generated_html = generate_html(resume_markdown, css)

    # write out generated html
    output_html_path = os.path.join(output_dir, "resume.html")
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(generated_html)
        logging.info(f"Written to: {f.name}")
