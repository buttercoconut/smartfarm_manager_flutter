import 'dart:async';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../models/sensor.dart';
import '../models/environment.dart';
import 'dart:convert';

class WebSocketService extends ChangeNotifier {
  final String _wsUrl = 'wss://ws.smartfarm.example.com';
  late WebSocketChannel _channel;
  final List<Sensor> _sensors = [];
  Environment? _environment;

  List<Sensor> get sensors => List.unmodifiable(_sensors);
  Environment? get environment => _environment;

  void connect() {
    _channel = WebSocketChannel.connect(Uri.parse(_wsUrl));
    _channel.stream.listen(_onMessage, onError: _onError, onDone: _onDone);
  }

  void _onMessage(dynamic message) {
    final Map<String, dynamic> data = jsonDecode(message as String);
    if (data['type'] == 'sensor') {
      final sensor = Sensor.fromJson(data['payload']);
      _sensors.add(sensor);
      notifyListeners();
    } else if (data['type'] == 'environment') {
      _environment = Environment.fromJson(data['payload']);
      notifyListeners();
    }
  }

  void _onError(error) {
    // Handle reconnection logic if needed
    print('WebSocket error: $error');
  }

  void _onDone() {
    // Attempt reconnection after a delay
    Future.delayed(const Duration(seconds: 5), () => connect());
  }

  void dispose() {
    _channel.sink.close();
    super.dispose();
  }
}
