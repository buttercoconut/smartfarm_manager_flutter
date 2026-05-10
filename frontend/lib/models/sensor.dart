class Sensor {
  final String id;
  final String type;
  final double value;
  final DateTime timestamp;

  Sensor({
    required this.id,
    required this.type,
    required this.value,
    required this.timestamp,
  });

  factory Sensor.fromJson(Map<String, dynamic> json) => Sensor(
        id: json['id'] as String,
        type: json['type'] as String,
        value: (json['value'] as num).toDouble(),
        timestamp: DateTime.parse(json['timestamp'] as String),
      );
}
