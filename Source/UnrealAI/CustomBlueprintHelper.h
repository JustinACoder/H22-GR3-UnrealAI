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

	//Lecture du Fichier
	UFUNCTION(BlueprintCallable)
		static FString getHangManWord(int index);

	//Lecture du Fichier
	UFUNCTION(BlueprintCallable, Category = "File I/O")
		static FString LoadFileToString(FString Filename);


	//Ecrire sur un fichier
	UFUNCTION(BlueprintCallable, Category = "File I/O")
		static FString SaveStringToFile(FString Filename, FString Data);
};
