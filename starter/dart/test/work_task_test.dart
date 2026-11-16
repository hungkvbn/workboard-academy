import 'dart:convert';

import 'package:test/test.dart';
import 'package:workboard_dart/workboard_dart.dart';

WorkTask task({String title = 'Học Dart', DateTime? dueAt}) => WorkTask(
      id: 't-1',
      title: title,
      dueAt: dueAt,
      updatedAt: DateTime.utc(2026, 1, 1),
      ownerId: 'u-1',
    );

void main() {
  test('Tiêu đề được trim', () {
    expect(task(title: '  Học Dart  ').title, 'Học Dart');
  });

  test('Từ chối tiêu đề chỉ có khoảng trắng', () {
    expect(() => task(title: ' \n '), throwsArgumentError);
  });

  test('Từ chối tiêu đề dài hơn 120 code units', () {
    expect(() => task(title: List.filled(121, 'a').join()), throwsArgumentError);
  });

  test('copyWith không đổi bản gốc', () {
    final original = task();
    final changed = original.copyWith(status: TaskStatus.done);
    expect(original.status, TaskStatus.todo);
    expect(changed.status, TaskStatus.done);
    expect(changed.id, original.id);
  });

  test('copyWith phân biệt giữ hạn và xóa hạn', () {
    final original = task(dueAt: DateTime.utc(2026, 2, 1));
    expect(original.copyWith(title: 'Tên mới').dueAt, original.dueAt);
    expect(original.copyWith(clearDueAt: true).dueAt, isNull);
  });

  test('JSON round trip giữ các trường', () {
    final original = task(dueAt: DateTime.utc(2026, 2, 1));
    final decoded = jsonDecode(jsonEncode(original.toJson()));
    final restored = WorkTask.fromJson((decoded as Map).cast<String, Object?>());
    expect(restored.toJson(), original.toJson());
  });

  test('Ngày có timezone được chuẩn hóa UTC', () {
    final parsed = DateTime.parse('2026-02-01T09:00:00+07:00');
    expect(task(dueAt: parsed).dueAt, DateTime.utc(2026, 2, 1, 2));
    expect(task(dueAt: parsed).dueAt!.isUtc, isTrue);
  });

  test('Trạng thái không hợp lệ không bị âm thầm đổi thành todo', () {
    expect(() => TaskStatus.fromJson('archived'), throwsFormatException);
  });
}
