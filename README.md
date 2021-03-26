# ValheimSaveEditor
Allows modification of the values inside a Valheim character save file. Make sure the game is closed, open your character's fch file, make modifications, and save. A backup of your original save file is made when you save, it'll be in the same location as your character files. Some values are limited by the game and will be brought back inline once the game loads the save. Have fun.

Currently supports modifying:
* Player Name
* Health/Stamina
* Misc Stats like kills, deaths, builds
* Guardian Power & current cooldown time
* Skill Levels & XP
* Inventory
  * Add or Delete Items
  * Stack size
  * Quality(upgrade level) of items
  * Crafter Name/ID
  * Durability
* Character Appearance
  * Skin/Hair color
  * Beard/Hair model
* Active Foods
  * Activate any food
  * Modify health and stamina received from food
* World Data
  * Change spawn/death/logout/home coordinates

For adding items to your inventory refer to this awesome list for item names:
[Spawn Item List by Demogrim](https://www.reddit.com/r/valheim/comments/lig8ml/spawn_item_command_list/)

Disabling Steam Cloud saves for Valheim is recommended. Use at your own risk. I am not responsible for any saves that are corrupted or lost while using this program.

### FAQ
__Increasing my max health/stamina or current health value doesn't raise it in game?__

A: Your max health is governed by your food, modify the health value of a food item, then match your current health value to that.

__My character is bald and has no clothes?__

A: Your save file was corrupted, this happens when one of the entered values isn't the right type(ie: text instead of a number) or a value is over/under the game's internal limit. Restore your backup and try again.

__Saving doesn't seem to do anything/When I load the new save nothing has changed:__

A: Steam's cloud service may be restoring your save file to it's pre-modified version. Right click Valheim in steam, go to properties, and uncheck "Keep game saves in the Steam Cloud for Valheim"

__Can skills be raised over 100?__

A: Yes, skills can go well over 100. Set your jump to 1000 and you'll feel like the Hulk. Fall damage is very real though.

__None of the tabs work:__

A: The tabs will only work once you've loaded in a save file
