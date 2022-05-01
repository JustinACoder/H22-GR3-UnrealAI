// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "IncludeActor.generated.h"

/**
* Base actor for the AI blueprint actor.
* Used to include files to remove a loading bug in the editor.
*/
UCLASS()
class UNREALAI_API AIncludeActor : public AActor
{
	GENERATED_BODY()

public:
	// Sets default values for this actor's properties
	AIncludeActor();

	// Machine learning component
	UPROPERTY(BlueprintReadWrite, VisibleAnywhere, Category = "Machine learning component")
		class UMachineLearningRemoteComponent* MLComponent;

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:
	// Called every frame
	virtual void Tick(float DeltaTime) override;

};
