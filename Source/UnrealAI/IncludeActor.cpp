// Fill out your copyright notice in the Description page of Project Settings.


#include "IncludeActor.h"
// File included to fix the editor bug
#include <MachineLearningRemoteComponent.h>

// Sets default values
AIncludeActor::AIncludeActor()
{
	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

	// Create the Machine Learning Component
	MLComponent = CreateDefaultSubobject<UMachineLearningRemoteComponent>(FName("MLComponent"));
}

// Called when the game starts or when spawned
void AIncludeActor::BeginPlay()
{
	Super::BeginPlay();

}

// Called every frame
void AIncludeActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}

