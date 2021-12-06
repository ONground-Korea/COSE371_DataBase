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
    course_id varchar(7) references course(course_id),
    prereq_id varchar(7) references course(course_id),
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
    instructor_id varchar(20) references instructor(instructor_id));
create table section_time (
    section_id int references section(id) not null,
    timeslot_id int references timeslot(id),
    place_id int references place(id)
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
    email varchar(30));
create table login (
    std_id varchar(10) references student(std_id) not null,
    id varchar(30) primary key,
    pw varchar(200) not null);
create table takes (
    std_id varchar(10) references student(std_id) not null,
    section_id int references section(id) not null,
    grade varchar(2) references grades(alphabet),
    primary key (std_id, section_id)
);

insert into college values ('정보대학');

insert into department values ('컴퓨터학과', '정보대학');
insert into department values ('정보보호융합전공', '정보대학');

insert into place values (default, '우정정보관', '101', null);

insert into timeslot values (default, 'monday', 1, '09:00:00', '10:15:00');

insert into grades values ('A+', 4.5);

insert into instructor values ('2020320001','이혁기', '정보대학','컴퓨터학과');
insert into instructor values ('2020320002', '김승룡', '정보대학', '컴퓨터학과');
insert into instructor values ('2020320003', '정원기', '정보대학', '컴퓨터학과');
insert into instructor values ('2020320004', '강재우','정보대학','컴퓨터학과');

insert into student values ('2020320078', '한지상', '정보대학', '컴퓨터학과', null, '2020320002', 'present', '01054968096', '서울시 도봉구 방학동', '01337', '20010214', 'jisang77747@gmail.com');
insert into login values ('2020320078', 'onground', 'fa585d89c851dd338a70dcf535aa2a92fee7836dd6aff1226583e88e0996293f16bc009c652826e0fc5c706695a03cddce372f139eff4d13959da6f1f5d3eabe');

insert into student values ('2020320044', '백민규', '정보대학', '컴퓨터학과', '정보보호융합전공', '2020320003', 'present', '01059231480', '서울시 강남구 일원동', '06344', '20010713', '0713jake@naver.com');
insert into login values ('2020320044', '0713jake', 'fa585d89c851dd338a70dcf535aa2a92fee7836dd6aff1226583e88e0996293f16bc009c652826e0fc5c706695a03cddce372f139eff4d13959da6f1f5d3eabe');

insert into login values ('2020320010', 'jbw', '00b884f39f8ff85732e20e05ce4b382fde04d79b28e40e8b7ff87709447f00e35ec3a488aaf23703f97a10b69a18c4161f87aa55b5e3afd09124c883341e78f0');

insert into course values ('COSE371','데이터베이스', '컴퓨터학과','major_required','3','3');
insert into section values (default, 'COSE371','02','2021','fall','2020320001');

insert into course values ('COSE362','기계학습','컴퓨터학과','major_elective','3','3');
insert into section values (default, 'COSE362','03','2021','FALL','2020320004');