// Fill out your copyright notice in the Description page of Project Settings.


#include "UnrealAIBlueprintFunctionLibrary.h"
#include "MyAiActor.h"

/**
* Call the function from the AI actor to communicate with the server.
**/
void UUnrealAIBlueprintFunctionLibrary::SendInputToServer(AMyAiActor* aiActor, TArray<float> inputImage)
{

	aiActor->SendInputToServer(inputImage);

}

