
def gravimetric_load(loaded_brutto, unloaded_brutto, tare_syr, molecular_weight):

    unloaded_resin=unloaded_brutto-tare_syr
    loaded_resin=loaded_brutto-tare_syr
    loaded_mass=loaded_resin-unloaded_resin
    loading_per_g=loaded_mass/((molecular_weight-36.431)*(loaded_resin)) *1000
    loading_total=loading_per_g*loaded_resin

    return loading_per_g, loading_total