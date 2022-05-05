// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "CustomBlueprintHelper.generated.h"

/**
 * 
 */
UCLASS()
class UNREALAI_API UCustomBlueprintHelper : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
		UFUNCTION(BlueprintCallable)
		static FString asciiToString(int asciiValue);
	UFUNCTION(BlueprintCallable)
		static FString getQuickDrawLabel(int maxIndex, float maxProbability, float minThresholdProbability);
};
