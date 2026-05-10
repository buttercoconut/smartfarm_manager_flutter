class Plant {
  final String id;
  final String name;
  final String species;
  final DateTime plantedAt;

  Plant({
    required this.id,
    required this.name,
    required this.species,
    required this.plantedAt,
  });

  factory Plant.fromJson(Map<String, dynamic> json) => Plant(
        id: json['id'] as String,
        name: json['name'] as String,
        species: json['species'] as String,
        plantedAt: DateTime.parse(json['plantedAt'] as String),
      );
}
