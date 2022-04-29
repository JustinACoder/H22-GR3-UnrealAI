// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "UnrealAIBlueprintFunctionLibrary.generated.h"

class AMyAiActor;

/**
 * Blueprint library for Unreal AI:
 *
 * Defines a function to send an input image to the server and 
 * do operations with the output of the model.
 */
UCLASS()
class UNREALAI_API UUnrealAIBlueprintFunctionLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

		UFUNCTION(BlueprintCallable, Category = "Unreal to Server Functions")
		static void SendInputToServer(AMyAiActor* aiActor, TArray<float> inputImage);
};
