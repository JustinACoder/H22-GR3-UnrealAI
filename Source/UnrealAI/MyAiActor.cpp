// Fill out your copyright notice in the Description page of Project Settings.


#include "MyAiActor.h"
#include <MachineLearningRemoteComponent.h>
#include <Json/Public/JsonGlobals.h>

// Sets default values
AMyAiActor::AMyAiActor()
{
	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

	// Create the component able to communicate with the server
	MLComponent = CreateDefaultSubobject<UMachineLearningRemoteComponent>(FName("MLComponent"));
}

// Called when the game starts or when spawned
void AMyAiActor::BeginPlay()
{
	Super::BeginPlay();

}

// Called every frame
void AMyAiActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}

void AMyAiActor::SendInputToServer(TArray<float> inputImage)
{

	// Send a float array to the server and apply the following function to the result
	MLComponent->SendRawInput(inputImage, [this](TArray<float>& result)
		{
			
			// Find the category with the highest value
			float max = 0;
			int category = 0;

			UE_LOG(LogTemp, Log, TEXT("Out of %i categories, "), result.Num());

			for (int i = 0; i < result.Num(); i++) {
				if (result[i] > max) {
					max = result[i];
					category = i;
				}
			}


			UE_LOG(LogTemp, Log, TEXT("The chosen category is : %i"), category);

		}, "on_json_input");
}

