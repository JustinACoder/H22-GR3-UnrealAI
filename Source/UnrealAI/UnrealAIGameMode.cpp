// Copyright Epic Games, Inc. All Rights Reserved.

#include "UnrealAIGameMode.h"
#include "UnrealAIHUD.h"
#include "UnrealAICharacter.h"
#include "UObject/ConstructorHelpers.h"

AUnrealAIGameMode::AUnrealAIGameMode()
	: Super()
{
	// set default pawn class to our Blueprinted character
	static ConstructorHelpers::FClassFinder<APawn> PlayerPawnClassFinder(TEXT("/Game/FirstPersonCPP/Blueprints/FirstPersonCharacter"));
	DefaultPawnClass = PlayerPawnClassFinder.Class;

	// use our custom HUD class
	HUDClass = AUnrealAIHUD::StaticClass();
}
