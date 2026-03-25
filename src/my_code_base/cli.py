#!/usr/bin/env python
# -*- coding utf-8 -*-
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-06-11
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#    
"""Console script for my-code-base."""

import typer
from rich.console import Console

app = typer.Typer()
console = Console()



@app.command()
def main():
    """CLI script for my_code_base."""
    console.print(r"""
  $$\      $$\           $$\                                             
  $$ | $\  $$ |          $$ |                                            
  $$ |$$$\ $$ | $$$$$$\  $$ | $$$$$$$\  $$$$$$\  $$$$$$\$$$$\   $$$$$$\  
  $$ $$ $$\$$ |$$  __$$\ $$ |$$  _____|$$  __$$\ $$  _$$  _$$\ $$  __$$\ 
  $$$$  _$$$$ |$$$$$$$$ |$$ |$$ /      $$ /  $$ |$$ / $$ / $$ |$$$$$$$$ |
  $$$  / \$$$ |$$   ____|$$ |$$ |      $$ |  $$ |$$ | $$ | $$ |$$   ____|
  $$  /   \$$ |\$$$$$$$\ $$ |\$$$$$$$\ \$$$$$$  |$$ | $$ | $$ |\$$$$$$$\ 
  \__/     \__| \_______|\__| \_______| \______/ \__| \__| \__| \_______|
                                                                      
    """, style="green")
    # https://patorjk.com/software/taag/
    console.print("Replace this message by putting your code into "
               "my_code_base.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")


if __name__ == "__main__":
    app()
