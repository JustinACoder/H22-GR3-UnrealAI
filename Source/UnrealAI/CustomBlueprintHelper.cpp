// Fill out your copyright notice in the Description page of Project Settings.

#include "CustomBlueprintHelper.h"

FString UCustomBlueprintHelper::asciiToString(int asciiValue)
{
	char a = 'A' + (asciiValue - 65);
	// cool trick, we add a value to 'A' so the compiler keeps the values as a char and then subtract the ascii value of A (65)
	return FString::Printf(TEXT("%c"), a);
}
