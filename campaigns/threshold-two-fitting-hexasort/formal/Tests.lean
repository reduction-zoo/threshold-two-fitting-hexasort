import Challenge
open ThresholdTwoFittingHexasort
example : targetWitness (⟨1,[]⟩,[0]) [0] = true := by native_decide
example : targetWitness (⟨1,[]⟩,[0,0]) [0,0] = false := by native_decide
example : targetWitness (⟨2,[(0,1)]⟩,[0,0,1]) [0,1,0] = true := by native_decide
