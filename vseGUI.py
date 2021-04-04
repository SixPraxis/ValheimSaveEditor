import PySimpleGUI as gui
import os.path
from vseCharacter import createCharacter
from vseUtils import backupSaveFile
from vseUtils import writeSaveFile
from vseItems import Food
from math import floor

appdataPath = os.getenv('APPDATA')
characterFolderPath = appdataPath[:-8] + '\\LocalLow\\IronGate\\Valheim\\characters'
title = 'Valheim Save Editor'
version = '1.0.4'
gui.theme('LightGrey3')
#gui.theme('DarkAmber')

menu_layout = [['File', ['Open::openKey', 'Save::saveKey', 'Exit']],
                ['About', ['About::aboutKey']]]

gLeftColumn = [[gui.Text('Character Name:'), gui.In(default_text='', size=(18,1), key='nameKey')],
        [gui.Text('Player Kills:'), gui.In(default_text='', size=(18,1), key='playerKillsKey')],
        [gui.Text('Deaths:'), gui.In(default_text='', size=(18,1), key='deathsKey')],
        [gui.Text('Crafts:'), gui.In(default_text='', size=(18,1), key='craftsKey')],
        [gui.Text('Builds:'), gui.In(default_text='', size=(18,1), key='buildsKey')],
        [gui.Text('PlayerID:'), gui.In(default_text='', size=(18,1), key='playerIdKey')],
        [gui.Text('Health:'), gui.In(default_text='', size=(18,1), key='healthKey')],
        [gui.Text('Max Health:'), gui.In(default_text='', size=(18,1), key='maxHealthKey')],
        [gui.Text('Max Stamina:'), gui.In(default_text='', size=(18,1), key='maxStaminaKey')],
        [gui.Text('TimeSinceDeath:'), gui.In(default_text='', size=(18,1), key='timeSinceDeathKey')],
        [gui.Text('Guardian Power:'), gui.Combo(values=['GP_Yagluth', 'GP_Moder', 'GP_Bonemass', 'GP_TheElder', 'GP_Eikthyr', 0], size=(14,1), key='guardianPowerKey')],
        [gui.Text('Power Cooldown:'), gui.In(default_text='', size=(18,1), key='powerCooldownKey')],
        ]

gRightColumn = [[gui.Text('Worlds Visited:'), gui.Text('', size=(5,1), key='worldsVisitedKey')],
        [gui.Text('Known Recipes:'), gui.Text('', size=(5,1), key='knownRecipesKey')],
        [gui.Text('Known Stations:'), gui.Text('', size=(5,1), key='knownStationsKey')],
        [gui.Text('Known Materials:'), gui.Text('', size=(5,1), key='knownMaterialsKey')],
        [gui.Text('Known Biomes:'), gui.Text('', size=(5,1), key='knownBiomesKey')],
        [gui.Text('Known Texts:'), gui.Text('', size=(5,1), key='knownTextsKey')],
        [gui.Text('Shown Tutorials:'), gui.Text('', size=(5,1), key='shownTutorialsKey')],
        [gui.Text('Uniques:'), gui.Text('', size=(5,1), key='uniquesKey')],
        [gui.Text('Trophies:'), gui.Text('', size=(5,1), key='trophiesKey')],
        ]

generalTabLayout = [[gui.Column(gLeftColumn, element_justification='right'), gui.VerticalSeparator(), gui.Column(gRightColumn, element_justification='right')]]

sLeftColumn = [[gui.Text('Swords:'), gui.In(default_text='', size=(18,1), key='swordsKey')],
        [gui.Text('Knives:'), gui.In(default_text='', size=(18,1), key='knivesKey')],
        [gui.Text('Clubs:'), gui.In(default_text='', size=(18,1), key='clubsKey')],
        [gui.Text('Polearms:'), gui.In(default_text='', size=(18,1), key='polearmsKey')],
        [gui.Text('Spears:'), gui.In(default_text='', size=(18,1), key='spearsKey')],
        [gui.Text('Blocking:'), gui.In(default_text='', size=(18,1), key='blockingKey')],
        [gui.Text('Axes:'), gui.In(default_text='', size=(18,1), key='axesKey')],
        [gui.Text('Bows:'), gui.In(default_text='', size=(18,1), key='bowsKey')],
        [gui.Text('Unarmed:'), gui.In(default_text='', size=(18,1), key='unarmedKey')],
        [gui.Text('Pickaxes:'), gui.In(default_text='', size=(18,1), key='pickaxesKey')],
        [gui.Text('Woodcutting:'), gui.In(default_text='', size=(18,1), key='woodcuttingKey')],
        [gui.Text('Jump:'), gui.In(default_text='', size=(18,1), key='jumpKey')],
        [gui.Text('Sneak:'), gui.In(default_text='', size=(18,1), key='sneakKey')],
        [gui.Text('Run:'), gui.In(default_text='', size=(18,1), key='runKey')],
        [gui.Text('Swim:'), gui.In(default_text='', size=(18,1), key='swimKey')],
        ]

sRightColumn = [[gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='swordsXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='knivesXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='clubsXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='polearmsXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='spearsXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='blockingXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='axesXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='bowsXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='unarmedXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='pickaxesXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='woodcuttingXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='jumpXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='sneakXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='runXPKey')],
        [gui.Text('XP:'), gui.In(default_text='', size=(18,1), key='swimXPKey')],
        ]

skillsTabLayout = [[gui.Text('Level Values: 0 - 100')],
        [gui.Text('XP is Reset Each Level')],
        [gui.Column(sLeftColumn, element_justification='right'), gui.VerticalSeparator(), gui.Column(sRightColumn, element_justification='left')]
        ]
        
inventorySlotColumnLayout = []
for i in range(0, 32):
    row = []
    key1 = 'slot' + str(i) + 'Key'
    key2 = 'slot' + str(i) + 'ItemKey'
    row.append(gui.Text('Slot ' + str(i) + ':', text_color='blue', relief='ridge', enable_events=True, key=key1))
    row.append(gui.Text('', size=(14, 1), key=key2))
    inventorySlotColumnLayout.append(row)

inventoryItemColumnLayout = [[gui.Text('Item:'), gui.In('', size=(18, 1), key='itemNameKey', enable_events=True),],
                [gui.Text('Stack:'), gui.In('', size=(18, 1), key='itemStackKey', enable_events=True)],
                [gui.Text('Durability:'), gui.In('', size=(18, 1), key='itemDurabilityKey', enable_events=True)],
                [gui.Text('PosX:'), gui.Text('', size=(15, 1), key='itemPosXKey')],
                [gui.Text('PosY:'), gui.Text('', size=(15, 1), key='itemPosYKey')],
                [gui.Text('Equipped:'), gui.Checkbox('', size=(12,1), key='itemEquippedKey', enable_events=True)],
                [gui.Text('Quality:'), gui.In('', size=(18, 1), key='itemQualityKey', enable_events=True)],
                [gui.Text('Variant:'), gui.In('', size=(18, 1), key='itemVariantKey', enable_events=True)],
                [gui.Text('CrafterID:'), gui.In('', size=(18, 1), key='itemCrafterIDKey', enable_events=True)],
                [gui.Text('CrafterName:'), gui.In('', size=(18, 1), key='itemCrafterNameKey', enable_events=True)],
                [gui.Button('New Item', visible=False, key='newItemButtonKey'), gui.Button('Submit', visible=False, key='submitButtonKey'), gui.Button('Delete', visible=False, key='deleteButtonKey')],
                ]

inventoryTabLayout = [[gui.Column(inventorySlotColumnLayout, element_justification='left', scrollable=True, vertical_scroll_only=True), gui.Column(inventoryItemColumnLayout, element_justification='right')]]

appearanceTabLayout = [[gui.Text('Model Type'), gui.Spin(values=[1, 0], initial_value='', size=(14,1), key='modelKey')],
            [gui.Text('_'*60)],
            [gui.Checkbox('Overload Mode', enable_events=True, key='overloadKey')],
            [gui.Text('Skin Color')],
            [gui.Text('Red:', size=(5, 1)), gui.Slider(range=(0, 100), size=(30, 15), orientation='h', key='skinVal1Key')],
            [gui.Text('Green:', size=(5, 1)), gui.Slider(range=(0, 100), size=(30, 15), orientation='h', key='skinVal2Key')],
            [gui.Text('Blue:', size=(5, 1)), gui.Slider(range=(0, 100), size=(30, 15), orientation='h', key='skinVal3Key')],
            [gui.Text('_'*60)],
            [gui.Text('Hair'), gui.Combo(values=['No Hair', 'Braided 1', 'Braided 2', 'Braided 3', 'Braided 4', 'Long 1', 'Ponytail 1', 'Ponytail 2', 'Ponytail 3', 'Ponytail 4', 'Short 1', 'Short 2', 'Side 1', 'Side 2', 'Side 3'], size=(14,1), key='hairKey')],
            [gui.Text('Beard'), gui.Combo(values=['No Beard', 'Braided 1', 'Braided 2', 'Braided 3', 'Braided 4', 'Long 1', 'Long 2', 'Short 1', 'Short 2', 'Short 3', 'Thick 1'], size=(14,1), key='beardKey')],
            [gui.Text('Hair Color')],
            [gui.Text('Red:', size=(5, 1)), gui.Slider(range=(0, 100), size=(30, 15), orientation='h', key='hairVal1Key')],
            [gui.Text('Green:', size=(5, 1)), gui.Slider(range=(0, 100), size=(30, 15), orientation='h', key='hairVal2Key')],
            [gui.Text('Blue:', size=(5, 1)), gui.Slider(range=(0, 100), size=(30, 15), orientation='h', key='hairVal3Key')],
            ]

foodList = list(Food.foodDict.keys())
foodTabLayout = [[gui.Text('Food 1')],
            [gui.Text('Item:'), gui.Combo(values=foodList, size=(14,1), enable_events=True, key='food1Key')],
            [gui.Text('Health:'), gui.In(size=(18,1), key='food1HealthKey')],
            [gui.Text('Stamina:'), gui.In(size=(18,1), key='food1StaminaKey')],
            [gui.Text('_'*60)],
            [gui.Text('Food 2')],
            [gui.Text('Item:'), gui.Combo(values=foodList, size=(14,1), enable_events=True, key='food2Key')],
            [gui.Text('Health:'), gui.In(size=(18,1), key='food2HealthKey')],
            [gui.Text('Stamina:'), gui.In(size=(18,1), key='food2StaminaKey')],
            [gui.Text('_'*60)],
            [gui.Text('Food 3')],
            [gui.Text('Item:'), gui.Combo(values=foodList, size=(14,1), enable_events=True, key='food3Key')],
            [gui.Text('Health:'), gui.In(size=(18,1), key='food3HealthKey')],
            [gui.Text('Stamina:'), gui.In(size=(18,1), key='food3StaminaKey')],
            ]

worldInfoColumnLeftLayout = [[gui.Checkbox('Custom Spawn', key='customSpawnBoolKey', enable_events=True)],
                [gui.Text('X:'), gui.In('', size=(15, 1), key='customSpawnXKey')], 
                [gui.Text('Y:'), gui.In('', size=(15, 1), key='customSpawnYKey')], 
                [gui.Text('Z:'), gui.In('', size=(15, 1), key='customSpawnZKey')],
                [gui.Checkbox('Logout Point', key='logoutBoolKey', enable_events=True)],
                [gui.Text('X:'), gui.In('', size=(15, 1), key='logoutXKey')], 
                [gui.Text('Y:'), gui.In('', size=(15, 1), key='logoutYKey')], 
                [gui.Text('Z:'), gui.In('', size=(15, 1), key='logoutZKey')]
                ]

worldInfoColumnRightLayout = [[gui.Checkbox('Death Point', key='deathBoolKey', enable_events=True)],
                [gui.Text('X:'), gui.In('', size=(15, 1), key='deathXKey')], 
                [gui.Text('Y:'), gui.In('', size=(15, 1), key='deathYKey')], 
                [gui.Text('Z:'), gui.In('', size=(15, 1), key='deathZKey')],
                [gui.Text('Home Point:')],
                [gui.Text('X:'), gui.In('', size=(15, 1), key='homeXKey')], 
                [gui.Text('Y:'), gui.In('', size=(15, 1), key='homeYKey')], 
                [gui.Text('Z:'), gui.In('', size=(15, 1), key='homeZKey')],]

worldsTabLayout = [[gui.Text('Worlds:')],
            [gui.Listbox(values='', size=(50, 5), select_mode='LISTBOX_SELECT_MODE_SINGLE',  enable_events=True, key = 'worldListKey')],
            [gui.Text('World Key:'), gui.Text('', size=(18, 1), key='worldKeyKey')],
            [gui.Text('Pin Count:'), gui.Text('', size=(18, 1), key='pinCountKey')],
            [gui.Column(worldInfoColumnLeftLayout, element_justification='left'), gui.VerticalSeparator(), gui.Column(worldInfoColumnRightLayout, element_justification='left')],
            [gui.Button('Submit', visible = False, key = 'worldSubmitButtonKey')]
            ]

layout = [[gui.Menu(menu_layout)],
        [gui.Text('Valheim Save Editor', font=('Helvetica', 20), justification="center", auto_size_text=True)],
        [gui.TabGroup([[gui.Tab('General', generalTabLayout, key='generalTabKey'), gui.Tab('Skills', skillsTabLayout, disabled = True, key='skillsTabKey'), gui.Tab('Inventory', inventoryTabLayout, disabled = True, key='inventoryTabKey'), gui.Tab('Appearance', appearanceTabLayout, disabled = True, key='appearanceTabKey'), gui.Tab('Food', foodTabLayout, disabled = True, key = 'foodTabKey'), gui.Tab('Worlds', worldsTabLayout, disabled = True, key = 'worldsTabKey')]])],
        [gui.Text('Status:'), gui.Text('No character loaded.', size=(50,1), key='statusKey')]
        ]

def startGUI():
    window = gui.Window(title, layout, margins=(10,10), finalize=True)
    path = ''
    character = None
    mostRecentSlot = ''
    mostRecentWorld = 0
    enabledStatus = False

    while True:
        event, values = window.read()
        if event == 'Open::openKey':
            path = gui.popup_get_file('', initial_folder=characterFolderPath, no_window=True)
            if path != '':
                if not enabledStatus:
                    window['skillsTabKey'].update(disabled = False)
                    window['inventoryTabKey'].update(disabled = False)
                    window['appearanceTabKey'].update(disabled = False)
                    window['foodTabKey'].update(disabled = False)
                    window['worldsTabKey'].update(disabled = False)
                    enabledStatus = True
                character = createCharacter(path)
                populateFields(character, window)
                window['statusKey'].update('Loaded ' + os.path.basename(path))
                window = window.Finalize()
        if event == 'Save::saveKey' and path != '' and character != None:
            backupSaveFile(path)
            updateCharacter(character, values)
            writeSaveFile(character, path)
            window['statusKey'].update('Saved ' + os.path.basename(path))
        if event != None:
            if 'slot' in event:
                mostRecentSlot = event[0:-3]
                updateItemColumn(event, values, character, window)
        if event == 'overloadKey':
            if values['overloadKey'] == True:
                overloadValues(window)
            if values['overloadKey'] == False:
                overloadValues(window, False)
        if event == 'submitButtonKey':
            window[mostRecentSlot + 'ItemKey'].update(values['itemNameKey'])
            updateItem(mostRecentSlot, values, character)
        if event == 'deleteButtonKey':
            deleteItem(mostRecentSlot, character, window)
        if event == 'newItemButtonKey':
            newItem(mostRecentSlot, character, window)
        if event =='food1Key' or event == 'food2Key' or event == 'food3Key':
            window[event[0:5] + 'HealthKey'].update(Food.foodDict[values[event]][0])
            window[event[0:5] + 'StaminaKey'].update(Food.foodDict[values[event]][1])
        if event == 'worldListKey':
            mostRecentWorld = window['worldListKey'].get_indexes()[0]
            populateWorldData(mostRecentWorld, character, window)
            window['worldSubmitButtonKey'].update(visible = True)
        if event == 'worldSubmitButtonKey':
            updateWorld(mostRecentWorld, values, character)
        if event == 'About::aboutKey':
            gui.Popup('Valheim Save Editor', 'Version: ' + version, 'Created by SixPraxis', 'github.com/SixPraxis')
        if event == gui.WIN_CLOSED or event == 'Exit':
            break

def hairTranslator(value, beardSwitch = False, nameSwitch = False):
    beardName = ['No Beard', 'Braided 1', 'Braided 2', 'Braided 3', 'Braided 4', 'Long 1', 'Long 2', 'Short 1', 'Short 2', 'Short 3', 'Thick 1']
    beardModel = ['BeardNone', 'Beard5', 'Beard6', 'Beard9', 'Beard10', 'Beard1', 'Beard2', 'Beard3', 'Beard4', 'Beard7', 'Beard8']
    hairName = ['No Hair', 'Braided 1', 'Braided 2', 'Braided 3', 'Braided 4', 'Long 1', 'Ponytail 1', 'Ponytail 2', 'Ponytail 3', 'Ponytail 4', 'Short 1', 'Short 2', 'Side 1', 'Side 2', 'Side 3']
    hairModel = ['HairNone', 'Hair3', 'Hair11', 'Hair12', 'Hair13', 'Hair6', 'Hair1', 'Hair2', 'Hair4', 'Hair7', 'Hair5', 'Hair8', 'Hair9', 'Hair10', 'Hair14']
    
    #BugFix for some hairless characters not having a beard or hair value
    try:
        if value == '':
            if beardSwitch:
                if nameSwitch:
                    value = 'No Beard'
                else:
                    value = 'BeardNone'
            else:
                if nameSwitch:
                    value = 'No Hair'
                else:
                    value = 'HairNone'

        if beardSwitch:
            if nameSwitch:
                index = beardName.index(value)
                return beardModel[index]
            else:
                index = beardModel.index(value)
                return beardName[index]
        else:
            if nameSwitch:
                index = hairName.index(value)
                return hairModel[index]
            else:
                index = hairModel.index(value)
                return hairName[index]
    except ValueError:
        return value


def populateFields(character, window):
    window['nameKey'].update(character.name)
    window['playerKillsKey'].update(character.kills)
    window['deathsKey'].update(character.deaths)
    window['craftsKey'].update(character.crafts)
    window['buildsKey'].update(character.builds)
    window['playerIdKey'].update(character.playerID)
    window['healthKey'].update(character.currentHealth)
    window['maxHealthKey'].update(character.maxHealth)
    window['maxStaminaKey'].update(character.maxStamina)
    window['timeSinceDeathKey'].update(character.timeSinceDeath)
    window['guardianPowerKey'].update(character.guardianPower)
    window['powerCooldownKey'].update(character.guardianPowerCooldown)
    window['worldsVisitedKey'].update(character.worldCount)
    window['knownRecipesKey'].update(len(character.knownRecipes))
    window['knownStationsKey'].update(len(character.knownStations))
    window['knownMaterialsKey'].update(len(character.knownMaterials))
    window['knownBiomesKey'].update(len(character.knownBiomes))
    window['knownTextsKey'].update(len(character.knownTexts))
    window['shownTutorialsKey'].update(len(character.shownTutorials))
    window['uniquesKey'].update(len(character.uniques))
    window['trophiesKey'].update(len(character.trophies))
    window['beardKey'].update(hairTranslator(character.beard, beardSwitch = True))
    window['hairKey'].update(hairTranslator(character.hair))
    window['modelKey'].update(character.playerModel)
    if (character.skinColor.val1 > 1) or (character.skinColor.val2 > 1) or (character.skinColor.val3 > 1) or (character.hairColor.val1 > 1) or (character.hairColor.val2 > 1) or (character.hairColor.val3 > 1):
        overloadValues(window)
    window['skinVal1Key'].update(character.skinColor.val1 * 100)
    window['skinVal2Key'].update(character.skinColor.val2 * 100)
    window['skinVal3Key'].update(character.skinColor.val3 * 100)
    window['hairVal1Key'].update(character.hairColor.val1 * 100)
    window['hairVal2Key'].update(character.hairColor.val2 * 100)
    window['hairVal3Key'].update(character.hairColor.val3 * 100)
    worldList = []
    for world in character.worlds:
        worldList.append(world.worldKey)
    window['worldListKey'].update(worldList)

    foodNum = 1
    for __ in character.foods:
        window['food' + str(foodNum) + 'Key'].update(character.foods[foodNum - 1][0])
        window['food' + str(foodNum) + 'HealthKey'].update(character.foods[foodNum - 1][1])
        window['food' + str(foodNum) + 'StaminaKey'].update(character.foods[foodNum - 1][2])
        foodNum += 1

    for skill, skillObject in vars(character.skills).items():
        if skill != 'frostmagic' and skill != 'firemagic':
            window[skill + 'Key'].update(skillObject.level)
            window[skill + 'XPKey'].update(skillObject.accumulator)
    
    for slot, item in character.inventory.slots.items():
        if item != None:
            window[slot + 'ItemKey'].update(item.name)
    
    # window[''].update(character.)

def updateCharacter(character, values):
    character.name = values['nameKey']
    character.kills = int(values['playerKillsKey'])
    character.deaths = int(values['deathsKey'])
    character.crafts = int(values['craftsKey'])
    character.builds = int(values['buildsKey'])
    character.playerID = int(values['playerIdKey'])
    character.currentHealth = float(values['healthKey'])
    character.maxHealth = float(values['maxHealthKey'])
    character.maxStamina = float(values['maxStaminaKey'])
    character.timeSinceDeath = float(values['timeSinceDeathKey'])
    character.guardianPower = values['guardianPowerKey']
    character.guardianPowerCooldown = float(values['powerCooldownKey'])
    character.beard = hairTranslator(values['beardKey'], True, True)
    character.hair = hairTranslator(values['hairKey'], False, True)
    character.playerModel = values['modelKey']
    character.skinColor.val1 = float(values['skinVal1Key'] / 100)
    character.skinColor.val2 = float(values['skinVal2Key'] / 100)
    character.skinColor.val3 = float(values['skinVal3Key'] / 100)
    character.hairColor.val1 = float(values['hairVal1Key'] / 100)
    character.hairColor.val2 = float(values['hairVal2Key'] / 100)
    character.hairColor.val3 = float(values['hairVal3Key'] / 100)
    
    foodArray = []
    if values['food1Key'] != 'None' and values['food1Key'] != '':
        food1 = [values['food1Key'], float(values['food1HealthKey']), float(values['food1StaminaKey'])]
        foodArray.append(food1)
    if values['food2Key'] != 'None' and values['food2Key'] != '':
        food2 = [values['food2Key'], float(values['food2HealthKey']), float(values['food2StaminaKey'])]
        foodArray.append(food2)
    if values['food3Key'] != 'None' and values['food3Key'] != '':
        food3 = [values['food3Key'], float(values['food3HealthKey']), float(values['food3StaminaKey'])]
        foodArray.append(food3)
    character.foods = foodArray
    for skill, skillObject in vars(character.skills).items():
        if skill != 'frostmagic' and skill != 'firemagic':
            skillObject.level = float(values[skill + 'Key'])
            skillObject.accumulator = float(values[skill + 'XPKey'])
    
    invCount = 0
    for __, item in character.inventory.slots.items():
        if item != None:
            invCount += 1
    character.inventoryCount = invCount

def updateItemColumn(event, values, character, window):
    eventSlot = event[0:-3]
    if window[eventSlot + 'ItemKey'].get() != '':
        item = character.inventory.slots[eventSlot]
        window['itemNameKey'].update(item.name, disabled = False)
        window['itemStackKey'].update(item.stackSize, disabled = False)
        window['itemDurabilityKey'].update(item.durability, disabled = False)
        window['itemPosXKey'].update(item.posX)
        window['itemPosYKey'].update(item.posY)
        window['itemEquippedKey'].update(item.equipped, disabled = False)
        window['itemQualityKey'].update(item.quality, disabled = False)
        window['itemVariantKey'].update(item.variant, disabled = False)
        window['itemCrafterIDKey'].update(item.crafterID, disabled = False)
        window['itemCrafterNameKey'].update(item.crafterName, disabled = False)
        window['submitButtonKey'].update(visible = True)
        window['deleteButtonKey'].update(visible = True)
        window['newItemButtonKey'].update(visible = False)
    else:
        posX = int(event[4:-3])%8
        posY = floor(int(event[4:-3])/8)
        window['itemPosXKey'].update(posX)
        window['itemPosYKey'].update(posY)
        window['itemNameKey'].update(disabled = True)
        window['itemStackKey'].update(disabled = True)
        window['itemDurabilityKey'].update(disabled = True)
        window['itemEquippedKey'].update(disabled = True)
        window['itemQualityKey'].update(disabled = True)
        window['itemVariantKey'].update(disabled = True)
        window['itemCrafterIDKey'].update(disabled = True)
        window['itemCrafterNameKey'].update(disabled = True)
        window['newItemButtonKey'].update(visible = True)
        window['submitButtonKey'].update(visible = False)
        window['deleteButtonKey'].update(visible = False)

def deleteItem(mostRecentSlot, character, window):
    character.inventory.slots[mostRecentSlot] = None
    window['itemNameKey'].update('')
    window['itemStackKey'].update('')
    window['itemDurabilityKey'].update('')
    window['itemPosXKey'].update('')
    window['itemPosYKey'].update('')
    window['itemEquippedKey'].update(0)
    window['itemQualityKey'].update('')
    window['itemVariantKey'].update('')
    window['itemCrafterIDKey'].update('')
    window['itemCrafterNameKey'].update('')
    window[mostRecentSlot + "ItemKey"].update('')
    window['submitButtonKey'].update(visible = False)

def newItem(mostRecentSlot, character, window):
    posX = int(mostRecentSlot[4::])%8
    posY = floor(int(mostRecentSlot[4::])/8)
    character.inventory.slots[mostRecentSlot] = character.inventory.createItem('New', 1, 100.0, posX, posY)
    item = character.inventory.slots[mostRecentSlot]
    window['itemNameKey'].update(item.name, disabled = False)
    window['itemStackKey'].update(item.stackSize, disabled = False)
    window['itemDurabilityKey'].update(item.durability, disabled = False)
    window['itemPosXKey'].update(item.posX)
    window['itemPosYKey'].update(item.posY)
    window['itemEquippedKey'].update(item.equipped, disabled = False)
    window['itemQualityKey'].update(item.quality, disabled = False)
    window['itemVariantKey'].update(item.variant, disabled = False)
    window['itemCrafterIDKey'].update(item.crafterID, disabled = False)
    window['itemCrafterNameKey'].update(item.crafterName, disabled = False)
    window[mostRecentSlot + "ItemKey"].update(item.name)
    window['newItemButtonKey'].update(visible = False)
    window['submitButtonKey'].update(visible = True)
    window['deleteButtonKey'].update(visible = True)

def updateItem(mostRecentSlot, values, character):
    character.inventory.slots[mostRecentSlot].name = values['itemNameKey']
    character.inventory.slots[mostRecentSlot].stackSize = int(values['itemStackKey'])
    character.inventory.slots[mostRecentSlot].durability = float(values['itemDurabilityKey'])
    character.inventory.slots[mostRecentSlot].equipped = bool(values['itemEquippedKey'])
    character.inventory.slots[mostRecentSlot].quality = int(values['itemQualityKey'])
    character.inventory.slots[mostRecentSlot].variant = int(values['itemVariantKey'])
    character.inventory.slots[mostRecentSlot].crafterID = int(values['itemCrafterIDKey'])
    character.inventory.slots[mostRecentSlot].crafterName = values['itemCrafterNameKey']

def updateWorld(mostRecentWorld, values, character):
    character.worlds[mostRecentWorld].customSpawnBool = values['customSpawnBoolKey']
    character.worlds[mostRecentWorld].spawnPoint[0] = float(values['customSpawnXKey'])
    character.worlds[mostRecentWorld].spawnPoint[1] = float(values['customSpawnYKey'])
    character.worlds[mostRecentWorld].spawnPoint[2] = float(values['customSpawnZKey'])
    character.worlds[mostRecentWorld].logoutPointBool = values['logoutBoolKey']
    character.worlds[mostRecentWorld].logoutPoint[0] = float(values['logoutXKey'])
    character.worlds[mostRecentWorld].logoutPoint[1] = float(values['logoutXKey'])
    character.worlds[mostRecentWorld].logoutPoint[2] = float(values['logoutXKey'])
    character.worlds[mostRecentWorld].deathPointBool = values['deathBoolKey']
    character.worlds[mostRecentWorld].deathPoint[0] = float(values['deathXKey'])
    character.worlds[mostRecentWorld].deathPoint[1] = float(values['deathYKey'])
    character.worlds[mostRecentWorld].deathPoint[2] = float(values['deathZKey'])
    character.worlds[mostRecentWorld].homePoint[0] = float(values['homeXKey'])
    character.worlds[mostRecentWorld].homePoint[1] = float(values['homeYKey'])
    character.worlds[mostRecentWorld].homePoint[2] = float(values['homeZKey'])

def populateWorldData(mostRecentWorld, character, window):
    window['worldKeyKey'].update(character.worlds[mostRecentWorld].worldKey)
    window['pinCountKey'].update(character.worlds[mostRecentWorld].mapData.pinCount)
    window['customSpawnBoolKey'].update(character.worlds[mostRecentWorld].customSpawnBool)
    window['customSpawnXKey'].update(character.worlds[mostRecentWorld].spawnPoint[0])
    window['customSpawnYKey'].update(character.worlds[mostRecentWorld].spawnPoint[1])
    window['customSpawnZKey'].update(character.worlds[mostRecentWorld].spawnPoint[2])
    window['logoutBoolKey'].update(character.worlds[mostRecentWorld].logoutPointBool)
    window['logoutXKey'].update(character.worlds[mostRecentWorld].logoutPoint[0])
    window['logoutYKey'].update(character.worlds[mostRecentWorld].logoutPoint[1])
    window['logoutZKey'].update(character.worlds[mostRecentWorld].logoutPoint[2])
    window['deathBoolKey'].update(character.worlds[mostRecentWorld].deathPointBool)
    window['deathXKey'].update(character.worlds[mostRecentWorld].deathPoint[0])
    window['deathYKey'].update(character.worlds[mostRecentWorld].deathPoint[1])
    window['deathZKey'].update(character.worlds[mostRecentWorld].deathPoint[2])
    window['homeXKey'].update(character.worlds[mostRecentWorld].homePoint[0])
    window['homeYKey'].update(character.worlds[mostRecentWorld].homePoint[1])
    window['homeZKey'].update(character.worlds[mostRecentWorld].homePoint[2])
    
def overloadValues(window, overload = True):
    if overload:
        window['skinVal1Key'].update(range=(0, 1000))
        window['skinVal2Key'].update(range=(0, 1000))
        window['skinVal3Key'].update(range=(0, 1000))
        window['hairVal1Key'].update(range=(0, 1000))
        window['hairVal2Key'].update(range=(0, 1000))
        window['hairVal3Key'].update(range=(0, 1000))
        window['overloadKey'].update(value=True)
    if not overload:
        window['skinVal1Key'].update(range=(0, 100))
        window['skinVal2Key'].update(range=(0, 100))
        window['skinVal3Key'].update(range=(0, 100))
        window['hairVal1Key'].update(range=(0, 100))
        window['hairVal2Key'].update(range=(0, 100))
        window['hairVal3Key'].update(range=(0, 100)) 
        window['overloadKey'].update(value=False)