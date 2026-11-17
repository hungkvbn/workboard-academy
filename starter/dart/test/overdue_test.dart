import 'package:test/test.dart';
import 'package:workboard_dart/workboard_dart.dart';

void main() {
  final now = DateTime.parse('2026-01-10T12:00:00Z');

  group('W01-L2: isOverdue', () {
    test('không có hạn thì không quá hạn', () {
      expect(isOverdue(now: now, isDone: false), isFalse);
    });
    test('hạn trước now và chưa hoàn thành thì quá hạn', () {
      expect(isOverdue(dueAt: now.subtract(const Duration(seconds: 1)),
          now: now, isDone: false), isTrue);
    });
    test('hạn bằng now không quá hạn', () {
      expect(isOverdue(dueAt: now, now: now, isDone: false), isFalse);
    });
    test('hạn sau now không quá hạn', () {
      expect(isOverdue(dueAt: now.add(const Duration(seconds: 1)),
          now: now, isDone: false), isFalse);
    });
    test('đã hoàn thành thì không quá hạn dù hạn đã qua', () {
      expect(isOverdue(dueAt: now.subtract(const Duration(days: 1)),
          now: now, isDone: true), isFalse);
    });
    test('hai múi giờ biểu diễn cùng thời điểm không quá hạn', () {
      expect(isOverdue(dueAt: DateTime.parse('2026-01-10T19:00:00+07:00'),
          now: now, isDone: false), isFalse);
    });
  }, skip: 'W01-L2 chưa làm: xóa skip khi bắt đầu lab rồi triển khai isOverdue.');
}
