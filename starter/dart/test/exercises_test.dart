import 'package:test/test.dart';
import 'package:workboard_dart/workboard_dart.dart';

WorkTask sample(String id, {TaskStatus status = TaskStatus.todo, DateTime? dueAt}) =>
    WorkTask(
      id: id,
      title: id == 'b' ? 'Đọc Flutter' : 'Học Dart',
      status: status,
      dueAt: dueAt,
      updatedAt: DateTime.utc(2026, 1, 1),
      ownerId: 'u-1',
    );

void main() {
  group('Bài tập tự làm W01–W02', () {
    test('normalizeTitle trim và kiểm tra biên', () {
      expect(normalizeTitle('  Học Dart \n'), 'Học Dart');
      expect(normalizeTitle('  '), '');
      expect(titleError('  '), isNotNull);
      expect(normalizeTitle(List.filled(120, 'a').join()).length, 120);
      expect(titleError(List.filled(120, 'a').join()), isNull);
      expect(titleError(List.filled(121, 'a').join()), isNotNull);
    });

    test('filterTasks kết hợp query và status, không thay đổi nguồn', () {
      final source = [sample('a'), sample('b'), sample('c', status: TaskStatus.done)];
      final result = filterTasks(source, status: TaskStatus.todo, query: ' DART ');
      expect(result.map((e) => e.id).toList(), ['a']);
      expect(source.map((e) => e.id).toList(), ['a', 'b', 'c']);
      expect(identical(result, source), isFalse);
    });

    test('filterTasks xử lý danh sách và query rỗng', () {
      expect(filterTasks([]), isEmpty);
      expect(filterTasks([sample('a')], query: '  ').length, 1);
    });

    test('sortTasks null ở cuối, cùng hạn dùng id, không sửa nguồn', () {
      final day = DateTime.utc(2026, 2, 1);
      final source = [sample('z'), sample('b', dueAt: day), sample('a', dueAt: day)];
      expect(sortTasks(source).map((e) => e.id).toList(), ['a', 'b', 'z']);
      expect(source.map((e) => e.id).toList(), ['z', 'b', 'a']);
      expect(sortTasks([]), isEmpty);
    });
  }, skip: 'Bài tập chưa làm. Xóa tham số skip sau khi đọc README và làm W01–W02.');
}
