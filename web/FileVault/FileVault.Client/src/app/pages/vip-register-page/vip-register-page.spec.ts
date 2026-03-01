import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VipRegisterPage } from './vip-register-page';

describe('VipRegisterPage', () => {
  let component: VipRegisterPage;
  let fixture: ComponentFixture<VipRegisterPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VipRegisterPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VipRegisterPage);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
