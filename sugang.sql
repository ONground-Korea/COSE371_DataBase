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

create table course (
    course_id varchar(7) primary key,
    course_name varchar(50),
    dept_name varchar(30) references department(dept_name),
    type varchar(4),
    credits numeric(1,0),
    hour numeric(1,0)
);
create table section (
    id varchar(50) primary key,
    course_id varchar(7) references course(course_id),
    section_id varchar(2),
    year numeric(4,0),
    semester varchar(10) check(semester in ('first', 'second', 'summer', 'winter')),
    instructor_name varchar(20) references instrutor(instructor_name));
create table student (
    std_id varchar(10) primary key,
    name varchar(20),
    college varchar(10) references college(college_name),
    first_major varchar(10) references department(dept_name),
    second_major varchar(10) references department(dept_name),
    std_instructor varchar(20) references instructor(instructor_name),
    std_status varchar(4),
    phone_number varchar(11),
    address varchar(100),
    zip_code varchar(10),
    birthday varchar(8),
    email varchar(30));
create table login (
    std_id varchar(10) references student(std_id),
    id varchar(30) primary key,
    pw varchar(30));
create table instructor (
    instructor_id varchar(10) primary key,
    instructor_name varchar(30),
    college_name varchar(10) references college(college_name),
    dept_name varchar(10) references department(dept_name)
);
create table takes (
    std_id varchar(10) references student(std_id),
    section_id varchar(50) references section(id),
    grade varchar(2) references grades(alphabet),
    primary key (std_id, section_id)
);
create table department (
    dept_name varchar(10) primary key,
    college_name varchar(10) references college(college_name)
);
create table college (
    college_name varchar(10) primary key
);
create table prereq (
    course_id varchar(7) references course(course_id),
    prereq_id varchar(7) references course(course_id),
    primary key (course_id, prereq_id)
);
create table place (
    building varchar(20),
    building_address varchar(10),
    building_name varchar(20),
    primary key (building, building_address)
);
create table section_time (
    section_id varchar(50) references section(id),
    hour numeric(1,0) references timeslot()
)