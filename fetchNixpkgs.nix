{ rev    ? "295cfcae856afc86d9c96057fcaa54def7716f18"             # The Git revision of nixpkgs to fetch
, sha256 ? "0k3kyzzi3wniir2rm92akbhl83sdg7lqgygs0cah90blfrymrxn8" # The SHA256 of the downloaded data
}:

builtins.fetchTarball {
  url = "https://github.com/airalab/airapkgs/archive/${rev}.tar.gz";
  inherit sha256;
}
