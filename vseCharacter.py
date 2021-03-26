from vseUtils import loadSaveFile

class VseCharacter:
    def __init__(self, characterData, worlds):
        self.opener = characterData[10]
        self.gameVersion = characterData[0]
        self.kills = characterData[1]
        self.deaths = characterData[2]
        self.crafts = characterData[3]
        self.builds = characterData[4]
        self.worldCount = characterData[5]
        self.name = characterData[6]
        self.playerID = characterData[7]
        self.startSeed = characterData[8]
        self.playerData = characterData[9]
        self.num = self.playerData[0]
        self.currentHealth = self.playerData[1]
        self.maxHealth = self.playerData[2]
        self.maxStamina = self.playerData[3]
        self.firstSpawn = self.playerData[4]
        self.timeSinceDeath = self.playerData[5]
        self.guardianPower = self.playerData[6]
        self.guardianPowerCooldown = self.playerData[7]
        self.invNum = self.playerData[8]
        self.inventoryCount = self.playerData[9]
        self.inventory = VseInventory(self.playerData[10])
        self.knownRecipes = self.playerData[11]
        self.knownStations = self.playerData[12]
        self.knownMaterials = self.playerData[13]
        self.shownTutorials = self.playerData[14]
        self.uniques = self.playerData[15]
        self.trophies = self.playerData[16]
        self.knownBiomes = self.playerData[17]
        self.knownTexts = self.playerData[18]
        self.beard = self.playerData[19]
        self.hair = self.playerData[20]
        self.skinColor = VseColorValues(self.playerData[21])
        self.hairColor = VseColorValues(self.playerData[22])
        self.playerModel = self.playerData[23]
        self.foods = self.playerData[24]
        self.skillNum = self.playerData[25]
        self.skills = VseSkillContainer(self.playerData[26])
        self.worlds = []
        for world in worlds:
            self.worlds.append(VseWorld(world))

class VseInventory:
    def __init__(self, inv):
        self.slots = {
        "slot0" : None,
        "slot1" : None,
        "slot2" : None,
        "slot3" : None,
        "slot4" : None,
        "slot5" : None,
        "slot6" : None,
        "slot7" : None,
        "slot8" : None,
        "slot9" : None,
        "slot10" : None,
        "slot11" : None,
        "slot12" : None,
        "slot13" : None,
        "slot14" : None,
        "slot15" : None,
        "slot16" : None,
        "slot17" : None,
        "slot18" : None,
        "slot19" : None,
        "slot20" : None,
        "slot21" : None,
        "slot22" : None,
        "slot23" : None,
        "slot24" : None,
        "slot25" : None,
        "slot26" : None,
        "slot27" : None,
        "slot28" : None,
        "slot29" : None,
        "slot30" : None,
        "slot31" : None
        }
        self.items = self.createAllItems(inv)
        self.assignInvSlots()
    
    def createAllItems(self, inv):
        items = []
        for item in inv:
            newItem = VseItem(item)
            items.append(newItem)
        return items

    def assignInvSlots(self):
        for item in self.items:
            slot = item.posY * 8 + item.posX
            self.slots['slot' + str(slot)] = item

    def createItem(self, name, stackSize, durability, posX, posY, equiped = 0, quality = 1, variant = 0, crafterID= 0, crafterName = ''):
        itemData = [name, stackSize, durability, posX, posY, equiped, quality, variant, crafterID, crafterName]
        return VseItem(itemData)


class VseItem:
    def __init__(self, itemData):
        self.name = itemData[0]
        self.stackSize = itemData[1]
        self.durability = itemData[2]
        self.posX = itemData[3]
        self.posY = itemData[4]
        self.equiped = itemData[5]
        self.quality = itemData[6]
        self.variant = itemData[7]
        self.crafterID = itemData[8]
        self.crafterName = itemData[9]

class VseSkillContainer:
    # skillDict = {
    #     'swords': 1,
    #     'knives': 2,
    #     'clubs': 3,
    #     'polearms': 4,
    #     'spears': 5,
    #     'blocking': 6,
    #     'axes': 7,
    #     'bows': 8,
    #     'firemagic': 9,
    #     'frostmagic': 10,
    #     'unarmed': 11,
    #     'pickaxes': 12,
    #     'woodcutting': 13,
    #     'jump': 100,
    #     'sneak': 101,
    #     'run': 102,
    #     'swim': 103
    # }
    def __init__(self, skills):
        self.swords = VseSkill([0, 0.0, 0.0])
        self.knives = VseSkill([0, 0.0, 0.0])
        self.clubs = VseSkill([0, 0.0, 0.0])
        self.polearms = VseSkill([0, 0.0, 0.0])
        self.spears = VseSkill([0, 0.0, 0.0])
        self.blocking = VseSkill([0, 0.0, 0.0])
        self.axes = VseSkill([0, 0.0, 0.0])
        self.bows = VseSkill([0, 0.0, 0.0])
        self.firemagic = VseSkill([0, 0.0, 0.0])
        self.frostmagic = VseSkill([0, 0.0, 0.0])
        self.unarmed = VseSkill([0, 0.0, 0.0])
        self.pickaxes = VseSkill([0, 0.0, 0.0])
        self.woodcutting = VseSkill([0, 0.0, 0.0])
        self.jump = VseSkill([0, 0.0, 0.0])
        self.sneak = VseSkill([0, 0.0, 0.0])
        self.run = VseSkill([0, 0.0, 0.0])
        self.swim = VseSkill([0, 0.0, 0.0])
        self.createSkills(skills)
    
    def getSkillArray(self):
        allSkills = [self.swords.getValues(), self.knives.getValues(), self.clubs.getValues(),
                        self.polearms.getValues(), self.spears.getValues(), self.blocking.getValues(),
                        self.axes.getValues(), self.bows.getValues(), self.unarmed.getValues(), self.pickaxes.getValues(),
                        self.woodcutting.getValues(), self.jump.getValues(), self.sneak.getValues(), self.run.getValues(),
                        self.swim.getValues()]
        return allSkills

    def createSkills(self, skills):
        for skill in skills:
            if skill[0] == 1:
                self.swords = VseSkill(skill)
            elif skill[0] == 2:
                self.knives = VseSkill(skill)
            elif skill[0] == 3:
                self.clubs = VseSkill(skill)
            elif skill[0] == 4:
                self.polearms = VseSkill(skill)
            elif skill[0] == 5:
                self.spears = VseSkill(skill)
            elif skill[0] == 6:
                self.blocking = VseSkill(skill)
            elif skill[0] == 7:
                self.axes = VseSkill(skill)
            elif skill[0] == 8:
                self.bows = VseSkill(skill)
            elif skill[0] == 9:
                self.firemagic = VseSkill(skill)
            elif skill[0] == 10:
                self.frostmagic = VseSkill(skill)
            elif skill[0] == 11:
                self.unarmed = VseSkill(skill)
            elif skill[0] == 12:
                self.pickaxes = VseSkill(skill)
            elif skill[0] == 13:
                self.woodcutting = VseSkill(skill)
            elif skill[0] == 100:
                self.jump = VseSkill(skill)
            elif skill[0] == 101:
                self.sneak = VseSkill(skill)
            elif skill[0] == 102:
                self.run = VseSkill(skill)
            elif skill[0] == 103:
                self.swim = VseSkill(skill)


class VseSkill:
    def __init__(self, skillData):
        self.type = skillData[0]
        self.level = skillData[1]
        self.accumulator = skillData[2]
        
    def getValues(self):
        values = [self.type, self.level, self.accumulator]
        return values

class VseColorValues:
    def __init__(self, colorTuple):
        self.val1 = colorTuple[0]
        self.val2 = colorTuple[1]
        self.val3 = colorTuple[2]
    
    def __repr__(self):
        return 'Val1: ' + str(self.val1) + ', Val2: ' + str(self.val2) + ', Val3: ' + str(self.val3)

class VseWorld:
    def __init__(self, world):
        self.worldKey = world[0]
        self.customSpawnBool = world[1]
        self.spawnPoint = world[2]
        self.logoutPointBool = world[3]
        self.logoutPoint = world[4]
        self.deathPointBool = world[5]
        self.deathPoint = world[6]
        self.homePoint = world[7]
        self.mapDataBool = world[8]
        self.mapDataLength = world[9]
        self.mapData = VseMapData(world[10])

class VseMapData:
    def __init__(self, mapData):
        self.num1 = mapData[0]
        self.num2 = mapData[1]
        self.explored = mapData[2]
        self.pinCount = mapData[3]
        self.pins = mapData[4]
        self.publicRef = mapData[5]

def createCharacter(path):
    characterData, worlds = loadSaveFile(path)
    character = VseCharacter(characterData, worlds)
    return character