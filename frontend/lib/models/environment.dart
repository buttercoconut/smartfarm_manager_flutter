class Environment {
  final double temperature;
  final double humidity;
  final double light;
  final DateTime timestamp;

  Environment({
    required this.temperature,
    required this.humidity,
    required this.light,
    required this.timestamp,
  });

  factory Environment.fromJson(Map<String, dynamic> json) => Environment(
        temperature: (json['temperature'] as num).toDouble(),
        humidity: (json['humidity'] as num).toDouble(),
        light: (json['light'] as num).toDouble(),
        timestamp: DateTime.parse(json['timestamp'] as String),
      );
}
