{ stdenv
, mkRosPackage
, python3Packages
, robonomics_comm-nightly
}:

mkRosPackage rec {
  name = "${pname}-${version}";
  pname = "voltaware_collector";
  version = "master";

  src = ./.;

  propagatedBuildInputs = with python3Packages; [ robonomics_comm-nightly pika flask flask_sqlalchemy ];

  meta = with stdenv.lib; {
    description = "Voltaware sensor energy consumption collector node";
    homepage = http://github.com/airalab/voltaware_collector;
    license = licenses.bsd3;
    maintainers = with maintainers; [ akru ];
  };
}
