create index 
ab on ba(a);
create index abc on bac(ac);

alter table abc add constraint fkey foreign key(a) references bc(a);
