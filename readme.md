# Gunpath generator for Cyberpunk Red

This script automates the process of the gunpath system from the Cyberpunk Red DLC [Toggle's Temple](https://rtalsoriangames.com/wp-content/uploads/2024/06/RTG-CPR-DLC-TogglesTemplev1.1.pdf)

## Usage

Running the script with no flags will take you through a series of prompts to pick a value from a table for each weapon attribute or let the script roll for you. Note that the tables are different from the ones in the DLC as they have been weighted to removed the nested die rolls.

For you speed freaks out there you can skip as many of the prompts as you want with flags. These flags are detailed in the table below.

| Flag | Usage |
| ---- | ---- |
| `-s --speed` | Skips the prompts entirely and rolls any attribute not set by other flags. Defaults to having not attachment (see `-a --attachment`) |
| `-m --manufacturer` | Takes an integer as an argument and uses that for the roll on the manufacturer table, skipping the prompt if speed flag not used. |
| `-t --type` | Takes an integer as an argument and uses that for the roll on the weapon type table, skipping the prompt if speed flag not used. |
| `-q --quality` | Takes an integer as an argument and uses that for the roll on the quality table, skipping the prompt if speed flag not used. |
| `-a --attachment` | If used with no argument, it simply adds an attachment roll to speed mode or skips the prompt for if the gun has an attachment. If supplied an integre as an argument it uses that for the roll on the attachment table, skipping the prompt if speed flag not used. |
| `-d --description` | Takes an integer as an argument and uses that for the roll on the description table, skipping the prompt if speed flag not used. |


## To-Do

- Set messages for help flag
- Allow post get edits in non-speed mode
- Pretty up the output
- "Madlibs" type function for gun names.