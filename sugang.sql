drop table course;
drop table section;
drop table student;
drop table login;
drop table instructor;
drop table takes;
drop table department;
drop table college;
drop table prereq;
drop table place;
drop table section_time;
drop table timeslot;
drop table grades;

create table college (
    college_name varchar(10) primary key
);
create table place (
    building varchar(20) not null,
    building_address varchar(4) not null,
    place_name varchar(20),
    primary key (building, building_address)
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
    instructor_name varchar(20) references instructor(instructor_id));
create table section_time (
    section_id int references section(id) not null,
    timeslot_id int references timeslot(id)
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
    zip_code varchar(10),
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