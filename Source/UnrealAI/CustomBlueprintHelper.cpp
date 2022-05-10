// Fill out your copyright notice in the Description page of Project Settings.

#include "CustomBlueprintHelper.h"
#include <string>
#include <Runtime\Core\Public\Misc\FileHelper.h>


FString UCustomBlueprintHelper::asciiToString(int asciiValue)
{
	char a = 'A' + (asciiValue - 65);
	// cool trick, we add a value to 'A' so the compiler keeps the values as a char and then subtract the ascii value of A (65)
	return FString::Printf(TEXT("%c"), a);
}

FString UCustomBlueprintHelper::getQuickDrawLabel(const int maxIndex, float maxProbability, float minThresholdProbability)
{
	const FString labels[345] = { "aircraft carrier", "airplane", "alarm clock", "ambulance", "angel", "animal migration", "ant", "anvil", "apple", "arm", "asparagus", "axe", "backpack", "banana", "bandage", "barn", "baseball bat", "baseball", "basket", "basketball", "bat", "bathtub", "beach", "bear", "beard", "bed", "bee", "belt", "bench", "bicycle", "binoculars", "bird", "birthday cake", "blackberry", "blueberry", "book", "boomerang", "bottlecap", "bowtie", "bracelet", "brain", "bread", "bridge", "broccoli", "broom", "bucket", "bulldozer", "bus", "bush", "butterfly", "cactus", "cake", "calculator", "calendar", "camel", "camera", "camouflage", "campfire", "candle", "cannon", "canoe", "car", "carrot", "castle", "cat", "ceiling fan", "cell phone", "cello", "chair", "chandelier", "church", "circle", "clarinet", "clock", "cloud", "coffee cup", "compass", "computer", "cookie", "cooler", "couch", "cow", "crab", "crayon", "crocodile", "crown", "cruise ship", "cup", "diamond", "dishwasher", "diving board", "dog", "dolphin", "donut", "door", "dragon", "dresser", "drill", "drums", "duck", "dumbbell", "ear", "elbow", "elephant", "envelope", "eraser", "eye", "eyeglasses", "face", "fan", "feather", "fence", "finger", "fire hydrant", "fireplace", "firetruck", "fish", "flamingo", "flashlight", "flip flops", "floor lamp", "flower", "flying saucer", "foot", "fork", "frog", "frying pan", "garden hose", "garden", "giraffe", "goatee", "golf club", "grapes", "grass", "guitar", "hamburger", "hammer", "hand", "harp", "hat", "headphones", "hedgehog", "helicopter", "helmet", "hexagon", "hockey puck", "hockey stick", "horse", "hospital", "hot air balloon", "hot dog", "hot tub", "hourglass", "house plant", "house", "hurricane", "ice cream", "jacket", "jail", "kangaroo", "key", "keyboard", "knee", "knife", "ladder", "lantern", "laptop", "leaf", "leg", "light bulb", "lighter", "lighthouse", "lightning", "line", "lion", "lipstick", "lobster", "lollipop", "mailbox", "map", "marker", "matches", "megaphone", "mermaid", "microphone", "microwave", "monkey", "moon", "mosquito", "motorbike", "mountain", "mouse", "moustache", "mouth", "mug", "mushroom", "nail", "necklace", "nose", "ocean", "octagon", "octopus", "onion", "oven", "owl", "paint can", "paintbrush", "palm tree", "panda", "pants", "paper clip", "parachute", "parrot", "passport", "peanut", "pear", "peas", "pencil", "penguin", "piano", "pickup truck", "picture frame", "pig", "pillow", "pineapple", "pizza", "pliers", "police car", "pond", "pool", "popsicle", "postcard", "potato", "power outlet", "purse", "rabbit", "raccoon", "radio", "rain", "rainbow", "rake", "remote control", "rhinoceros", "rifle", "river", "roller coaster", "rollerskates", "sailboat", "sandwich", "saw", "saxophone", "school bus", "scissors", "scorpion", "screwdriver", "sea turtle", "see saw", "shark", "sheep", "shoe", "shorts", "shovel", "sink", "skateboard", "skull", "skyscraper", "sleeping bag", "smiley face", "snail", "snake", "snorkel", "snowflake", "snowman", "soccer ball", "sock", "speedboat", "spider", "spoon", "spreadsheet", "square", "squiggle", "squirrel", "stairs", "star", "steak", "stereo", "stethoscope", "stitches", "stop sign", "stove", "strawberry", "streetlight", "string bean", "submarine", "suitcase", "sun", "swan", "sweater", "swing set", "sword", "syringe", "t-shirt", "table", "teapot", "teddy-bear", "telephone", "television", "tennis racquet", "tent", "The Eiffel Tower", "The Great Wall of China", "The Mona Lisa", "tiger", "toaster", "toe", "toilet", "tooth", "toothbrush", "toothpaste", "tornado", "tractor", "traffic light", "train", "tree", "triangle", "trombone", "truck", "trumpet", "umbrella", "underwear", "van", "vase", "violin", "washing machine", "watermelon", "waterslide", "whale", "wheel", "windmill", "wine bottle", "wine glass", "wristwatch", "yoga", "zebra", "zigzag" };
	if (maxProbability < minThresholdProbability || maxIndex < 0 || maxIndex >= 345) {
		return FString(TEXT("?")); // not clear enough
	}

	// we got a match!
	return labels[maxIndex];
}

FString UCustomBlueprintHelper::getHangManWord(int index)
{
	const FString words[100] = { "legs", "body", "glass", "motion", "notebook", "pail", "harbor", "sock", "distance", "cork",
		"winter", "pollution", "hand", "religion", "head", "agreement", "wing", "sign", "tongue", "stream",
		"shirt", "curve", "giants", "mitten", "riddle", "moon", "bun", "basketball", "connection", "screw",
	"quicksand", "plot", "way", "mouth", "carriage", "hand", "title", "trousers", "tent", "position",
	"boundary", "laugh", "ladybug", "swim", "stage", "kittens", "clocks", "bikes", "tiger", "border",
	"slave", "protest", "expert", "passenger", "end", "lake", "power", "heart", "arm", "arch", "group",
	"comb", "copper", "pocket", "tiger", "example", "silver", "leaf", "print", "help", "bee", "sink",
	"agreement", "beam", "receipt", "trail", "knee", "eyes", "mitten", "smoke", "limit", "trick", "waves",
	"reading", "notebook", "laborer", "industry", "suit", "balloon", "children", "engine", "kiss", "string",
	"field", "plot", "arm", "ant", "discovery" };

	if (index > 100 || index < 0) return "?";
	else return words[index];
}

FString UCustomBlueprintHelper::LoadFileToString(FString Filename)
{
	FString directory = FPaths::GameSourceDir();
	FString result;
	IPlatformFile& file = FPlatformFileManager::Get().GetPlatformFile();

	if (file.CreateDirectory(*directory))
	{
		FString myFile = directory + "/" + Filename;
		FFileHelper::LoadFileToString(result, *myFile);
	}
	return result;
}

FString UCustomBlueprintHelper::SaveStringToFile(FString Filename, FString Data)
{
	FString directory = FPaths::GameSourceDir();
	FString result;

	IPlatformFile& file = FPlatformFileManager::Get().GetPlatformFile();

	if (file.CreateDirectory(*directory))
	{
		FString myFile = directory + "/" + Filename;
		FFileHelper::SaveStringToFile(Data, *myFile);
	}
	return Filename;
}
