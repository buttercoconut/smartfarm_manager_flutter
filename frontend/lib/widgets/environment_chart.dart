import 'package:flutter/material.dart';
import 'package:charts_flutter/flutter.dart' as charts;
import '../../models/environment.dart';

class EnvironmentChart extends StatelessWidget {
  final List<Environment> data;

  const EnvironmentChart({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    final series = [
      charts.Series<Environment, DateTime>(
        id: 'Temperature',
        colorFn: (_, __) => charts.MaterialPalette.red.shadeDefault,
        domainFn: (Environment env, _) => env.timestamp,
        measureFn: (Environment env, _) => env.temperature,
        data: data,
      ),
      charts.Series<Environment, DateTime>(
        id: 'Humidity',
        colorFn: (_, __) => charts.MaterialPalette.blue.shadeDefault,
        domainFn: (Environment env, _) => env.timestamp,
        measureFn: (Environment env, _) => env.humidity,
        data: data,
      ),
      charts.Series<Environment, DateTime>(
        id: 'Light',
        colorFn: (_, __) => charts.MaterialPalette.yellow.shadeDefault,
        domainFn: (Environment env, _) => env.timestamp,
        measureFn: (Environment env, _) => env.light,
        data: data,
      ),
    ];

    return SizedBox(
      height: 200,
      child: charts.TimeSeriesChart(
        series,
        animate: true,
        dateTimeFactory: const charts.LocalDateTimeFactory(),
        behaviors: [
          charts.SeriesLegend(),
          charts.ChartTitle('Environment Over Time',
              behaviorPosition: charts.BehaviorPosition.top),
        ],
      ),
    );
  }
}
