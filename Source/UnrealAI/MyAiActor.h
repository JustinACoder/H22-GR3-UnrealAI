// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MyAiActor.generated.h"

UCLASS()
class UNREALAI_API AMyAiActor : public AActor
{
	GENERATED_BODY()

public:
	// Sets default values for this actor's properties
	AMyAiActor();

	UPROPERTY(BlueprintReadWrite, VisibleAnywhere, Category = "Machine learning component")
		class UMachineLearningRemoteComponent* MLComponent;

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:
	// Called every frame
	virtual void Tick(float DeltaTime) override;

	void SendInputToServer(TArray<float> inputImage);

};
