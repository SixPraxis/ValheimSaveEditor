""" vseUtils.py: File handling and data parsing methods for Valheim Character Editor \n
    Methods: \n
    loadSaveFile() - Accepts path to Valheim character save file. Returns two arrays with parsed data. \n
    readSaveFile() - Read byte values from Valheim character save file. Returns two arrays with binary data. \n
    parseCharacterData() - Convert byte values from characterData into integers and strings. Returns array with parsed data. \n
    parseWorldsData() - Convert byte values from worlds into integers and strings. Returns array with parsed data. \n
    addStringToFormat() - Reads bytes to determine String length. Adds proper length String format character to a format string.\n
    intPatternLoop() - Determine number of objects from leading Int value, then follows specified struct pattern to extract them.\n
    stringDecoder() - Convert binary data into Strings and strip leading char. \n
    stringEncoder() - \n
    backupSaveFile() - \n
    writeSaveFile() - \n
    intPatternLoopToBytes()
"""
import struct
from shutil import copyfile
from time import time_ns
from hashlib import sha512
from math import floor

def loadSaveFile(path):
    # Handle character save file and return extracted values
    with open(path, 'rb') as file:
        unparsedCharData, unparsedWorlds = readSaveFile(file)
    
    characterData = parseCharacterData(unparsedCharData)
    worlds = parseWorldsData(unparsedWorlds)
    return characterData, worlds

def readSaveFile(file):
    # Extract binary values from save file
    # Reference: PlayerProfile.LoadPlayerFromDisk() in assembly_valheim.dll
    opener = file.read(4)
    gameVersion = file.read(4)
    playerKills = file.read(4)
    playerDeaths = file.read(4)
    playerCrafts = file.read(4)
    playerBuilds = file.read(4)
    worldKeyCount = file.read(4)
    worlds = []

    for __ in range(int.from_bytes(worldKeyCount, 'little')):
        worldKey = file.read(8)
        customSpawnBool = file.read(1)
        spawnPoint = file.read(12)
        logoutPointBool = file.read(1)
        logoutPoint = file.read(12)
        deathPointBool = file.read(1)
        deathPoint = file.read(12)
        homePoint = file.read(12)
        mapDataBool = file.read(1)
        mapDataLength = file.read(4)
        mapData = file.read(int.from_bytes(mapDataLength, 'little'))

        worldData = [worldKey, customSpawnBool, spawnPoint, 
                    logoutPointBool, logoutPoint, deathPointBool, 
                    deathPoint, homePoint, mapDataBool, mapDataLength, mapData]
        worlds.append(worldData)

    nameLength = int.from_bytes(file.read(1), 'little')
    playerName = file.read(nameLength)
    playerID = file.read(8)
    seedLength = int.from_bytes(file.read(1), 'little')
    startSeed = file.read(seedLength)

    playerData = None
    if int.from_bytes(file.read(1), 'little') == 1:
        playerDataLength = int.from_bytes(file.read(4), 'little')
        playerData = file.read(playerDataLength)

    characterData = [gameVersion, playerKills, playerDeaths, 
                playerCrafts, playerBuilds, worldKeyCount, 
                playerName, playerID, startSeed, playerData, opener]
    
    #count2 = int.from_bytes(file.read(4), 'little')
    #sha512Hash = int.from_bytes(file.read(count2), 'little')

    return characterData, worlds

def parseCharacterData(characterData):
    # Convert extracted byte values into integers and strings
    for index in range(6):
        characterData[index] = int.from_bytes(characterData[index], 'little')

    characterData[6] = characterData[6].decode("utf-8")        
    characterData[7] = int.from_bytes(characterData[7], 'little')
    characterData[8] = characterData[8].decode("utf-8")
    
    # Reference Player.Load() in assembly_valheim.dll for playerData parsing
    formatString = '<Ifff?f'
    buffer = characterData[9]
    offset = struct.calcsize(formatString)
    formatString = addStringToFormat(formatString, buffer, offset)
    formatString += 'fII'

    num, maxHealth, currentHealth, maxStamina, firstSpawn, timeSinceDeath, guardianPower, guardianPowerCooldown, invNum, inventoryCount = struct.unpack_from(formatString, buffer, 0)
    
    guardianPower = guardianPower[1::].decode('utf-8')
    
    # Reference Inventory.Load() for inventory parsing
    offset = struct.calcsize(formatString)
    inventory = []
    #Process each item and add to inventory array, adjust offset for next iteration of loop
    for __ in range(inventoryCount):
        itemFormatString = '<'
        itemFormatString = addStringToFormat(itemFormatString, buffer, offset)
        itemFormatString += 'IfII?IIQ'
        tempOffset = offset + struct.calcsize(itemFormatString)
        itemFormatString = addStringToFormat(itemFormatString, buffer, tempOffset)

        text, stack, durability, posX, posY, equiped, quality, variant, crafterID, crafterName = struct.unpack_from(itemFormatString, buffer, offset)
        
        item = [text[1::].decode('utf-8'), stack, durability, posX, posY, equiped, quality, variant, crafterID, crafterName[1::].decode('utf-8')]
        inventory.append(item)
        
        offset += struct.calcsize(itemFormatString)

    knownRecipes, offset = intPatternLoop(buffer, offset)
    knownStations, offset = intPatternLoop(buffer, offset, 'sI')
    knownMaterials, offset = intPatternLoop(buffer, offset)
    shownTutorials, offset = intPatternLoop(buffer, offset)
    uniques, offset = intPatternLoop(buffer, offset)
    trophies, offset = intPatternLoop(buffer, offset)
    knownBiomes, offset = intPatternLoop(buffer, offset, 'I')
    knownTexts, offset = intPatternLoop(buffer, offset, 'ss')

    beardFormat = addStringToFormat('<', buffer, offset)
    beard = struct.unpack_from(beardFormat, buffer, offset)[0].decode('utf-8')[1::]
    offset += struct.calcsize(beardFormat)

    hairFormat = addStringToFormat('<', buffer, offset)
    hair = struct.unpack_from(hairFormat, buffer, offset)[0].decode('utf-8')[1::]
    offset += struct.calcsize(hairFormat)
    
    hairColor = struct.unpack_from('<fff', buffer, offset)
    offset += struct.calcsize('<fff')

    skinColor = struct.unpack_from('<fff', buffer, offset)
    offset += struct.calcsize('<fff')

    playerModel = struct.unpack_from('<I', buffer, offset)[0]
    offset += struct.calcsize('<I')

    foods, offset = intPatternLoop(buffer, offset, 'sff')

    skillNum = struct.unpack_from('<I', buffer, offset)[0]
    offset += struct.calcsize('<I')

    skills, offset = intPatternLoop(buffer, offset, 'Iff')

    playerData = [num, currentHealth, maxHealth, maxStamina, firstSpawn, 
                timeSinceDeath, guardianPower, guardianPowerCooldown, 
                invNum, inventoryCount, inventory, knownRecipes, 
                knownStations, knownMaterials, shownTutorials, 
                uniques, trophies, knownBiomes, knownTexts, beard, hair, 
                skinColor, hairColor, playerModel, foods, skillNum, skills]
    
    characterData[9] = playerData
    return characterData

def parseWorldsData(worlds):
    # Reference Minimap.GetMapData()
    # Reference Minimap.SetMapData()
    parsedWorlds = []
    for world in worlds:
        tempWorld = []
        tempWorld.append(int.from_bytes(world[0], 'little'))
        tempWorld.append(bool.from_bytes(world[1], 'little'))
        tempWorld.append(list(struct.unpack('<fff', world[2])))
        tempWorld.append(bool.from_bytes(world[3], 'little'))
        tempWorld.append(list(struct.unpack('<fff', world[4])))
        tempWorld.append(bool.from_bytes(world[5], 'little'))
        tempWorld.append(list(struct.unpack('<fff', world[6])))
        tempWorld.append(list(struct.unpack('<fff', world[7])))
        tempWorld.append(bool.from_bytes(world[8], 'little'))
        tempWorld.append(int.from_bytes(world[9], 'little'))
        num, num2 = struct.unpack_from('<II', world[10], 0)
        mapSize = num2 * num2
        offset = struct.calcsize('<II')
        mapGrid = struct.unpack_from(str(mapSize) + 's', world[10], offset)[0]
        offset += struct.calcsize(str(mapSize) + 's')
        pinCount = struct.unpack_from('<I', world[10], offset)[0]
        offset += struct.calcsize('<I')
        pinArray = []
        for __ in range(0, pinCount):
            formatString = '<'
            formatString = addStringToFormat(formatString, world[10], offset)
            formatString += 'fffI?'
            pinName, posX, posY, posZ, pinType, isChecked = struct.unpack_from(formatString, world[10], offset)
            pin = [pinName[1::].decode(), posX, posY, posZ, pinType, isChecked]
            pinArray.append(pin)
            offset += struct.calcsize(formatString)

        publicReference = struct.unpack_from('<?', world[10], offset)[0]
        mapDataArray = [num, num2, mapGrid, pinCount, pinArray, publicReference]
        tempWorld.append(mapDataArray)
        parsedWorlds.append(tempWorld)
    return parsedWorlds

def addStringToFormat(formatString, buffer, offset):
    stringLength = int.from_bytes(buffer[offset:offset + 1], 'little')
    formatString += str(stringLength + 1) + 's'
    return formatString

def intPatternLoop(buffer, offset, pattern = 's'):
    # Read amount of objects from first loop, then unpack objects based on pattern.
    # Only supports unsigned Int(I), String(s), and Float/Single(f)
    # Properly formats strings
    objCount = struct.unpack_from('<I', buffer, offset)[0]
    offset += struct.calcsize('<I')
    objArray = []
    for __ in range(objCount):
        obj = []
        objFormatString = '<'
        if pattern[0] == 's':
            objFormatString = addStringToFormat(objFormatString, buffer, offset)
        elif pattern[0] == 'I':
            objFormatString += 'I'
        if len(pattern) >= 2:
            if pattern[1] == 's':
                objFormatString = addStringToFormat(objFormatString, buffer, offset + struct.calcsize(objFormatString))
            elif pattern[1] == 'I':
                objFormatString += 'I'
            elif pattern[1] == 'f':
                objFormatString += 'f'
            if len(pattern) >= 3:
                if pattern[2] == 'f':
                    objFormatString += 'f'
        
        # Store unpacked values in arrays instead of tuples in order to allow formatting
        if len(pattern) == 1:
            obj = [struct.unpack_from(objFormatString, buffer, offset)[0]]
        elif len(pattern) == 2:
            val1, val2 = struct.unpack_from(objFormatString, buffer, offset)
            obj.append(val1)
            obj.append(val2)
        elif len(pattern) == 3:
            val1, val2, val3 = struct.unpack_from(objFormatString, buffer, offset)
            obj.append(val1)
            obj.append(val2)
            obj.append(val3)

        obj = stringDecoder(obj, pattern)
        objArray.append(obj)
        offset += struct.calcsize(objFormatString)


    return objArray, offset

def stringDecoder(obj, pattern):
    # Decode binary strings and strip leading character(leading character indicates string length)
    if pattern.count('s') > 0:
        index = pattern.find('s')
        obj[index] = obj[index].decode('utf-8')
        obj[index] = obj[index][1::]
        if pattern.count('s') > 1:
            index = pattern.find('s', index + 1)
            obj[index] = obj[index].decode('utf-8')
            obj[index] = obj[index][1::]
    
    return obj

def stringEncoder(string):
    length = len(string)
    pattern = 'B' + str(int(length)) + 's'
    string = string.encode('utf-8')
    return pattern, length, string

def backupSaveFile(path):
    copyPath = path + '.' + str(time_ns()) + '.BACKUP'
    copyfile(path, copyPath)

def writeSaveFile(character, path):
    data1 = struct.pack('<IIIIII', character.gameVersion, character.kills, character.deaths, character.crafts,
        character.builds, character.worldCount)

    worldByteArray = bytearray()
    for world in character.worlds:
        worldData2 = struct.pack('<II', world.mapData.num1, world.mapData.num2)
        worldData3 = world.mapData.explored
        worldData4 = struct.pack('<I', world.mapData.pinCount)
        worldData5 = bytearray()
        for pin in world.mapData.pins:
            pinNamePattern, pinNameInt, pinName = stringEncoder(pin[0])
            worldData5 += struct.pack('<' + pinNamePattern + 'fffI?', pinNameInt, pinName, pin[1], pin[2], pin[3], pin[4], pin[5])
        pubRef = world.mapData.pins
        worldData6 = struct.pack('<?', pubRef)
        world.mapDataLength = len(worldData2 + worldData3 + worldData4 + worldData5 + worldData6)
        worldData1 = struct.pack('<Q?fff?fff?ffffff?I', world.worldKey, world.customSpawnBool, world.spawnPoint[0], world.spawnPoint[1], world.spawnPoint[2], world.logoutPointBool, world.logoutPoint[0], world.logoutPoint[1], world.logoutPoint[2], world.deathPoint, world.deathPoint[0], world.deathPoint[1], world.deathPoint[2], world.homePoint[0], world.homePoint[1], world.homePoint[2], world.mapDataBool, world.mapDataLength)
        worldByteArray += worldData1 + worldData2 + worldData3 + worldData4 + worldData5 + worldData6


    namePattern, nameInt, name = stringEncoder(character.name)
    seedPattern, seedInt, seed = stringEncoder(character.startSeed)
    guardianPattern, guardianInt, guardian = stringEncoder(character.guardianPower)

    data2 = struct.pack('<' + namePattern + 'Q' + seedPattern + '?', nameInt, name, 
        character.playerID, seedInt, seed, True)

    playerDataBytes = bytearray()

    playerDataBytes += struct.pack('<Ifff?f' + guardianPattern + 'fII', character.num, 
        character.currentHealth, character.maxHealth, 
        character.maxStamina, character.firstSpawn, character.timeSinceDeath, 
        guardianInt, guardian, character.guardianPowerCooldown, character.invNum, character.inventoryCount)

    inventoryBytes = bytearray()

    for __, item in character.inventory.slots.items():
        if item != None:
            itemPattern = '<'
            textPattern, textInt, text = stringEncoder(item.name)
            crafterNamePattern, crafterNameInt, crafterName = stringEncoder(item.crafterName)
            itemPattern += textPattern + 'IfII?IIQ' + crafterNamePattern
            inventoryBytes += struct.pack(itemPattern, textInt, text, item.stackSize, item.durability, item.posX, item.posY, item.equiped, item.quality, item.variant, item.crafterID, crafterNameInt, crafterName)

    playerDataBytes += inventoryBytes
    playerDataBytes += intPatternLoopToBytes(character.knownRecipes)
    playerDataBytes += intPatternLoopToBytes(character.knownStations, 'sI')
    playerDataBytes += intPatternLoopToBytes(character.knownMaterials)
    playerDataBytes += intPatternLoopToBytes(character.shownTutorials)
    playerDataBytes += intPatternLoopToBytes(character.uniques)
    playerDataBytes += intPatternLoopToBytes(character.trophies)
    playerDataBytes += intPatternLoopToBytes(character.knownBiomes, 'I')
    playerDataBytes += intPatternLoopToBytes(character.knownTexts, 'ss')

    beardPattern, beardInt, beard = stringEncoder(character.beard)
    playerDataBytes += struct.pack('<' + beardPattern, beardInt, beard)

    hairPattern, hairInt, hair = stringEncoder(character.hair)
    playerDataBytes += struct.pack('<' + hairPattern, hairInt, hair)

    playerDataBytes += struct.pack('<fff', character.hairColor.val1, character.hairColor.val2, character.hairColor.val3)
    playerDataBytes += struct.pack('<fff', character.skinColor.val1, character.skinColor.val2, character.skinColor.val3)
    playerDataBytes += struct.pack('<I', character.playerModel)

    playerDataBytes += intPatternLoopToBytes(character.foods, 'sff')

    playerDataBytes += struct.pack('<I', character.skillNum)
    playerDataBytes += intPatternLoopToBytes(character.skills.getSkillArray(), 'Iff')

    playerDataLengthBytes = struct.pack('<I', len(playerDataBytes))

    opener = struct.pack('<I', len(data1 + worldByteArray + data2 + playerDataLengthBytes + playerDataBytes))
    h = sha512()
    h.update(data1 + worldByteArray + data2 + playerDataLengthBytes + playerDataBytes)
    sha512hash = h.hexdigest().encode('utf-8')
    
    with open(path, 'wb') as file:
        file.write(opener)
        file.write(data1)
        file.write(worldByteArray)
        file.write(data2)
        file.write(playerDataLengthBytes)
        file.write(playerDataBytes)
        file.write(struct.pack('<I', 64))
        file.write(sha512hash)

def intPatternLoopToBytes(characterAttrArray, patternString = 's'):
    length = len(characterAttrArray)
    dataBlock = b''
    dataBlock += struct.pack('<I', length)
    for obj in characterAttrArray:
        if patternString[0] == 's':
            objPattern, objStringLength, objString = stringEncoder(obj[0])
            dataBlock += struct.pack('<' + objPattern, objStringLength, objString)
        elif patternString[0] == 'I':
            dataBlock += struct.pack('<I', obj[0])
        if len(patternString) >= 2:
            if patternString[1] == 's':
                objPattern, objStringLength, objString = stringEncoder(obj[1])
                dataBlock += struct.pack('<' + objPattern, objStringLength, objString)
            elif patternString[1] == 'I':
                dataBlock += struct.pack('<I', obj[1])
            elif patternString[1] == 'f':
                dataBlock+= struct.pack('<f', obj[1])
        if len(patternString) >= 3:
            if patternString[2] == 'f':
                dataBlock += struct.pack('<f', obj[2])

    return dataBlock

