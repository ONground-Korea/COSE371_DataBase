drop table takes;
drop table login;
drop table student;
drop table section_time;
drop table section;
drop table instructor;
drop table prereq;
drop table course;
drop table department;
drop table grades;
drop table timeslot;
drop table place;
drop table college;

create table college (
    college_name varchar(10) primary key
);
create table place (
    id serial primary key,
    building varchar(20) not null,
    building_address varchar(4) not null,
    place_name varchar(20)
);
create table timeslot (
    id serial primary key,
    day varchar(9) check(day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')),
    period int check(period>=1),
    start_time time not null,
    end_time time not null
);
create table grades (
    alphabet varchar(2) primary key,
    number numeric(2, 1) check(number>=0.0) not null
);
create table department (
    dept_name varchar(10) primary key,
    college_name varchar(10) references college(college_name) not null
);
create table course (
    course_id varchar(7) primary key,
    course_name varchar(50) not null,
    dept_name varchar(30) references department(dept_name) not null,
    type varchar(14) check(type in ('major_required', 'major_elective', 'elective')) not null,
    credits int check(credits>=0) not null,
    hour int check(hour>=0) not null
);
create table prereq (
    course_id varchar(7) references course(course_id) on delete cascade,
    prereq_id varchar(7) references course(course_id) on delete cascade,
    primary key (course_id, prereq_id)
);
create table instructor (
    instructor_id varchar(10) primary key,
    instructor_name varchar(30) not null,
    college_name varchar(10) references college(college_name) not null,
    dept_name varchar(10) references department(dept_name) not null
);
create table section (
    id serial primary key,
    course_id varchar(7) references course(course_id),
    section_id varchar(2),
    year int check(year>=1905),
    semester varchar(6) check(semester in ('spring', 'summer', 'fall', 'winter')),
    instructor_id varchar(20) references instructor(instructor_id)
);
create table section_time (
    section_id int references section(id) not null,
    timeslot_id int references timeslot(id),
    place_id int references place(id),
    primary key(section_id, timeslot_id)
);
create table student (
    std_id varchar(10) primary key,
    name varchar(20) not null,
    college varchar(10) references college(college_name) not null,
    first_major varchar(10) references department(dept_name) not null,
    second_major varchar(10) references department(dept_name),
    std_instructor varchar(20) references instructor(instructor_id) not null,
    std_status varchar(7) check(std_status in ('present', 'absent', 'kicked')) not null,
    phone_number varchar(11),
    address varchar(100),
    zip_code char(5),
    birthday date not null,
    email varchar(30)
);
create table login (
    std_id varchar(10) references student(std_id) on delete cascade not null,
    id varchar(30) primary key,
    pw varchar(200) not null
);
create table takes (
    std_id varchar(10) references student(std_id) on delete cascade not null,
    section_id int references section(id) not null,
    grade varchar(2) references grades(alphabet),
    primary key (std_id, section_id)
);

insert into college values ('정보대학');
insert into college values ('정경대학');

insert into department values ('컴퓨터학과', '정보대학');
insert into department values ('정보보호융합전공', '정보대학');
insert into department values ('통계학과', '정경대학');

insert into place values (default, '우정정보관', '101', null);

insert into timeslot values (default, 'monday', 1, '09:00:00', '10:15:00');
insert into timeslot values (default, 'monday', 2, '10:30:00', '11:45:00');
insert into timeslot values (default, 'monday', 3, '12:00:00', '12:50:00');
insert into timeslot values (default, 'monday', 4, '13:00:00', '13:50:00');
insert into timeslot values (default, 'monday', 5, '14:00:00', '15:15:00');
insert into timeslot values (default, 'monday', 6, '15:30:00', '16:45:00');
insert into timeslot values (default, 'monday', 7, '17:00:00', '17:50:00');
insert into timeslot values (default, 'monday', 8, '18:00:00', '18:50:00');
insert into timeslot values (default, 'monday', 9, '19:00:00', '19:50:00');
insert into timeslot values (default, 'monday', 10, '20:00:00', '20:50:00');
insert into timeslot values (default, 'monday', 11, '21:00:00', '21:50:00');

insert into timeslot values (default, 'tuesday', 1, '09:00:00', '10:15:00');
insert into timeslot values (default, 'tuesday', 2, '10:30:00', '11:45:00');
insert into timeslot values (default, 'tuesday', 3, '12:00:00', '12:50:00');
insert into timeslot values (default, 'tuesday', 4, '13:00:00', '13:50:00');
insert into timeslot values (default, 'tuesday', 5, '14:00:00', '15:15:00');
insert into timeslot values (default, 'tuesday', 6, '15:30:00', '16:45:00');
insert into timeslot values (default, 'tuesday', 7, '17:00:00', '17:50:00');
insert into timeslot values (default, 'tuesday', 8, '18:00:00', '18:50:00');
insert into timeslot values (default, 'tuesday', 9, '19:00:00', '19:50:00');
insert into timeslot values (default, 'tuesday', 10, '20:00:00', '20:50:00');
insert into timeslot values (default, 'tuesday', 11, '21:00:00', '21:50:00');

insert into timeslot values (default, 'wednesday', 1, '09:00:00', '10:15:00');
insert into timeslot values (default, 'wednesday', 2, '10:30:00', '11:45:00');
insert into timeslot values (default, 'wednesday', 3, '12:00:00', '12:50:00');
insert into timeslot values (default, 'wednesday', 4, '13:00:00', '13:50:00');
insert into timeslot values (default, 'wednesday', 5, '14:00:00', '15:15:00');
insert into timeslot values (default, 'wednesday', 6, '15:30:00', '16:45:00');
insert into timeslot values (default, 'wednesday', 7, '17:00:00', '17:50:00');
insert into timeslot values (default, 'wednesday', 8, '18:00:00', '18:50:00');
insert into timeslot values (default, 'wednesday', 9, '19:00:00', '19:50:00');
insert into timeslot values (default, 'wednesday', 10, '20:00:00', '20:50:00');
insert into timeslot values (default, 'wednesday', 11, '21:00:00', '21:50:00');

insert into timeslot values (default, 'thursday', 1, '09:00:00', '10:15:00');
insert into timeslot values (default, 'thursday', 2, '10:30:00', '11:45:00');
insert into timeslot values (default, 'thursday', 3, '12:00:00', '12:50:00');
insert into timeslot values (default, 'thursday', 4, '13:00:00', '13:50:00');
insert into timeslot values (default, 'thursday', 5, '14:00:00', '15:15:00');
insert into timeslot values (default, 'thursday', 6, '15:30:00', '16:45:00');
insert into timeslot values (default, 'thursday', 7, '17:00:00', '17:50:00');
insert into timeslot values (default, 'thursday', 8, '18:00:00', '18:50:00');
insert into timeslot values (default, 'thursday', 9, '19:00:00', '19:50:00');
insert into timeslot values (default, 'thursday', 10, '20:00:00', '20:50:00');
insert into timeslot values (default, 'thursday', 11, '21:00:00', '21:50:00');

insert into timeslot values (default, 'friday', 1, '09:00:00', '10:15:00');
insert into timeslot values (default, 'friday', 2, '10:30:00', '11:45:00');
insert into timeslot values (default, 'friday', 3, '12:00:00', '12:50:00');
insert into timeslot values (default, 'friday', 4, '13:00:00', '13:50:00');
insert into timeslot values (default, 'friday', 5, '14:00:00', '15:15:00');
insert into timeslot values (default, 'friday', 6, '15:30:00', '16:45:00');
insert into timeslot values (default, 'friday', 7, '17:00:00', '17:50:00');
insert into timeslot values (default, 'friday', 8, '18:00:00', '18:50:00');
insert into timeslot values (default, 'friday', 9, '19:00:00', '19:50:00');
insert into timeslot values (default, 'friday', 10, '20:00:00', '20:50:00');
insert into timeslot values (default, 'friday', 11, '21:00:00', '21:50:00');

insert into timeslot values (default, 'saturday', 1, '09:00:00', '10:15:00');
insert into timeslot values (default, 'saturday', 2, '10:30:00', '11:45:00');
insert into timeslot values (default, 'saturday', 3, '12:00:00', '12:50:00');
insert into timeslot values (default, 'saturday', 4, '13:00:00', '13:50:00');
insert into timeslot values (default, 'saturday', 5, '14:00:00', '15:15:00');
insert into timeslot values (default, 'saturday', 6, '15:30:00', '16:45:00');
insert into timeslot values (default, 'saturday', 7, '17:00:00', '17:50:00');
insert into timeslot values (default, 'saturday', 8, '18:00:00', '18:50:00');
insert into timeslot values (default, 'saturday', 9, '19:00:00', '19:50:00');
insert into timeslot values (default, 'saturday', 10, '20:00:00', '20:50:00');
insert into timeslot values (default, 'saturday', 11, '21:00:00', '21:50:00');

insert into timeslot values (default, 'sunday', 1, '09:00:00', '10:15:00');
insert into timeslot values (default, 'sunday', 2, '10:30:00', '11:45:00');
insert into timeslot values (default, 'sunday', 3, '12:00:00', '12:50:00');
insert into timeslot values (default, 'sunday', 4, '13:00:00', '13:50:00');
insert into timeslot values (default, 'sunday', 5, '14:00:00', '15:15:00');
insert into timeslot values (default, 'sunday', 6, '15:30:00', '16:45:00');
insert into timeslot values (default, 'sunday', 7, '17:00:00', '17:50:00');
insert into timeslot values (default, 'sunday', 8, '18:00:00', '18:50:00');
insert into timeslot values (default, 'sunday', 9, '19:00:00', '19:50:00');
insert into timeslot values (default, 'sunday', 10, '20:00:00', '20:50:00');
insert into timeslot values (default, 'sunday', 11, '21:00:00', '21:50:00');

insert into grades values ('A+', 4.5);
insert into grades values ('A', 4.0);
insert into grades values ('B+', 3.5);
insert into grades values ('B', 3.0);
insert into grades values ('C+', 2.5);
insert into grades values ('C', 2.0);
insert into grades values ('D+', 1.5);
insert into grades values ('D', 1.0);
insert into grades values ('F', 0.0);
insert into grades values ('P', 0.0);

insert into instructor values ('2020320001','이혁기', '정보대학','컴퓨터학과');
insert into instructor values ('2020320002', '김승룡', '정보대학', '컴퓨터학과');
insert into instructor values ('2020320003', '정원기', '정보대학', '컴퓨터학과');
insert into instructor values ('2020320004', '강재우','정보대학','컴퓨터학과');
insert into instructor values ('2020320005', '정순영','정보대학','컴퓨터학과');
insert into instructor values ('2020320006', '김현철','정보대학','컴퓨터학과');
insert into instructor values ('2020320007', '육동석','정보대학','컴퓨터학과');
insert into instructor values ('2020320008', '김선희','정보대학','컴퓨터학과');
insert into instructor values ('2020320009', '김진규','정보대학','컴퓨터학과');
insert into instructor values ('2020320010', '박성빈','정보대학','컴퓨터학과');
insert into instructor values ('2020320011', '서태원','정보대학','컴퓨터학과');
insert into instructor values ('2020320012', '구건재','정보대학','컴퓨터학과');
insert into instructor values ('2020320013', '정성우','정보대학','컴퓨터학과');
insert into instructor values ('2020320014', '민성기','정보대학','컴퓨터학과');
insert into instructor values ('2020320015', '김효곤','정보대학','컴퓨터학과');
insert into instructor values ('2020320016', '이도길','정보대학','컴퓨터학과');

insert into student values ('2020320078', '한지상', '정보대학', '컴퓨터학과', null, '2020320002', 'present', '01054968096', '서울특별시 도봉구 방학동', '01337', '20010214', 'jisang77747@gmail.com');
insert into login values ('2020320078', 'onground', 'fa585d89c851dd338a70dcf535aa2a92fee7836dd6aff1226583e88e0996293f16bc009c652826e0fc5c706695a03cddce372f139eff4d13959da6f1f5d3eabe');

insert into student values ('2020320044', '백민규', '정보대학', '컴퓨터학과', '정보보호융합전공', '2020320003', 'present', '01059231480', '서울특별시 강남구 일원동', '06344', '20010713', '0713jake@naver.com');
insert into login values ('2020320044', '0713jake', 'fa585d89c851dd338a70dcf535aa2a92fee7836dd6aff1226583e88e0996293f16bc009c652826e0fc5c706695a03cddce372f139eff4d13959da6f1f5d3eabe');

insert into student values ('2020320010', '전병우', '정보대학', '컴퓨터학과', '통계학과', '2020320003', 'present', '01012341480', '서울특별시 중구 황학동', '12345', '19980623', 'ipcs@naver.com');
insert into login values ('2020320010', 'jbw', '00b884f39f8ff85732e20e05ce4b382fde04d79b28e40e8b7ff87709447f00e35ec3a488aaf23703f97a10b69a18c4161f87aa55b5e3afd09124c883341e78f0');

insert into course values ('COSE371','데이터베이스', '컴퓨터학과','major_required',3,3);
insert into section values (default, 'COSE371','01','2021','fall','2020320005');
insert into section values (default, 'COSE371','02','2021','fall','2020320001');
insert into section_time values (2, 18, 1);
insert into section_time values (2, 19, 1);
insert into section_time values (2, 40, 1);

insert into course values ('COSE213', '자료구조', '컴퓨터학과', 'major_required', 3, 3);
insert into section values (default, 'COSE213', '01', '2021', 'fall','2020320003');
insert into section values (default, 'COSE213', '02', '2021', 'fall','2020320008');


insert into course values ('COSE101', '컴퓨터프로그래밍I', '컴퓨터학과', 'elective', 3, 3);

insert into course values ('COSE102', '컴퓨터프로그래밍II', '컴퓨터학과', 'elective', 3, 3);

insert into prereq values ('COSE371', 'COSE213');
insert into prereq values ('COSE371', 'COSE101');
insert into prereq values ('COSE371', 'COSE102');
insert into prereq values ('COSE213', 'COSE101');
insert into prereq values ('COSE213', 'COSE102');

insert into course values ('COSE362','기계학습','컴퓨터학과','major_elective',3,3);
insert into section values (default, 'COSE362','01','2021','fall','2020320007');
insert into section values (default, 'COSE362','02','2021','fall','2020320006');
insert into section values (default, 'COSE362','03','2021','fall','2020320004');

insert into takes values ('2020320078', 2, 'A+');
insert into takes values ('2020320044', 2, 'A+');
insert into takes values ('2020320010', 2, 'A+');
insert into takes values ('2020320078', 5, 'A');